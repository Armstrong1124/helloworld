import os
import re
import sys
import logging
import time
from datetime import datetime
from subprocess import Popen, PIPE
import pandas as pd


os.environ['NUMEXPR_MAX_THREADS'] = '16'

HOUR = 1
SPECIFIC = 1  # 指定路径写1，不指定路径遍历跑写0
GET_BAG_INFO = 1  # 执行rosbag info命令记录时长信息写1，不记录写0
COPY_TO_REMOTE = 1  # 生成的csv从本地copy到nas写1，不复制就存在本地写0
USER_DIR = os.path.expanduser('~')  # 不要用sudo命令执行脚本，不用手动更改用户目录

if SPECIFIC:
    SRC0 = sys.argv[1]
    DST0 = sys.argv[2]
else:
    SRC1 = os.path.join(USER_DIR, 'nas/01_测试数据/05_2944前角雷达/00_常规路测')
    SRC2 = os.path.join(USER_DIR, 'nas/01_测试数据/05_2944前角雷达/02_跟踪算法需求数据')
    SRC3 = os.path.join(USER_DIR, 'nas/01_测试数据/05_2944前角雷达/06_场景')
    DST1 = os.path.join(USER_DIR, 'nas/CornerRadarDatabase')
    DST2 = os.path.join(USER_DIR, 'nas/标准场景')

CSV_PATH = os.path.join(USER_DIR, 'nas/CornerRadarDatabase')
RECORDING_DIR = 'dimension'
RECORDED_DIR = 'database'
os.makedirs(RECORDING_DIR, exist_ok=True)
os.makedirs(RECORDED_DIR, exist_ok=True)
PATTERN_DURATION = re.compile(r'duration:\s*(.*)')
PATTERN_SIZE = re.compile(r'size:.*?(\d+.\d+.*?GB)')
PATTERN_TIME = re.compile(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
PATTERN_BAG = re.compile(r'.*?_.*?_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
DATA_TIME_FRAME = {
    '66ms': ['2023-11-06-16-09-53', '2023-11-24-12-13-04'],
    '80ms': ['2023-10-27-10-03-21', '2023-11-05-10-54-16'],
    '100ms': ['2023-10-17-15-15-50', '2023-10-23-17-21-19'],
}
COLUMNS = ['car', 'path', 'bag', 'bag_duration', 'scene_names', 'scene_types', 'road_types', 'vehicle_types',
           'autopilot_status', 'side_status', 'tunnel_status', 'weather_status']


def get_logger():
    lg = logging.getLogger()
    lg.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s-line%(lineno)d-%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    lg.addHandler(console_handler)
    return lg


logger = get_logger()


def ros_data_exist(path_list, folder):
    for f in path_list:
        if folder in f:
            return True
    return False


def save_csv(df, path):
    if not os.path.exists(path):
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, index=False, header=False, mode='a')


def ros_data_copy(src_path, dst_path, recorded_data_path):
    recorded_data = pd.read_csv(recorded_data_path)
    if 'bag_duration' not in recorded_data.columns:
        recorded_data.insert(3, 'bag_duration', '')
    filename = os.path.basename(src_path)
    if ros_data_exist(recorded_data['path'], filename):
        logger.info(f'{filename} data exists, no need to copy')
        return

    recording_data = list()

    for roots, dirs, files in os.walk(src_path):
        for f in files:
            if not f.endswith('.bag'):
                continue
            curr_bag_path = os.path.join(roots, f)
            cmd = f'rosbag info {curr_bag_path}'
            column_bag_duration = ''
            if GET_BAG_INFO:
                try:
                    start = time.time()
                    resp = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = resp.communicate()
                    pattern_str = stdout.decode()
                    column_bag_duration = re.findall(PATTERN_DURATION, pattern_str)[0].split(' ')[-1].replace('(', '').replace(')', '').replace('s', '')
                    logger.info(f'{f} duration: {column_bag_duration}, read time: {int(time.time() - start)}s')
                except Exception as e:
                    logger.warning(f'{curr_bag_path} read error, {e}')
            if re.match(PATTERN_BAG, f):
                column_car = f.split('/')[-1].split('_')[0]
            else:
                column_car = '-'
            column_path = os.path.join(dst_path.replace(USER_DIR, ''), filename, curr_bag_path.split(filename)[1].lstrip('/'))
            columns_label_status = [''] * 8
            recording_data.append([column_car, column_path, f, column_bag_duration] + columns_label_status)

    try:
        recording_data = pd.DataFrame(recording_data, columns=COLUMNS)
        recording_data = recording_data.sort_values(by='bag')
        recorded_data = pd.concat((recorded_data, recording_data))
        recording_data[recording_data == ''] = 0

        recorded_data_save_path = os.path.join(RECORDED_DIR, os.path.basename(recorded_data_path))
        recording_data_save_path = os.path.join(RECORDING_DIR, os.path.basename(recorded_data_path))

        save_csv(recorded_data, recorded_data_save_path)
        save_csv(recording_data, recording_data_save_path)
        if COPY_TO_REMOTE:
            os.system(f'sudo cp -r {RECORDING_DIR} {CSV_PATH}')
            os.system(f'sudo cp -r {RECORDED_DIR} {CSV_PATH}')
            os.system(f'sudo cp -r {src_path} {dst_path}')
        logger.info(f'{src_path} copy to {dst_path} finish!')
    except Exception as e:
        logger.warning(e)
        if os.path.exists(dst_path):
            os.removedirs(dst_path)
            logger.info(f'{dst_path} remove success')


def date2timestamp(date, fmt="%Y-%m-%d-%H-%M-%S"):
    dt = datetime.strptime(date, fmt)
    return int(time.mktime(dt.timetuple()))


def get_time(src_path):
    record_time = -1
    upload_time = -1
    for r, d, f in os.walk(src_path):
        for bag in f:
            if not bag.endswith('.bag'):
                continue
            try:
                curr_bag_time = re.findall(PATTERN_TIME, bag)[0]
                record_time = max(record_time, date2timestamp(curr_bag_time))
                curr_bag_path = os.path.join(r, bag)
                upload_time = max(upload_time, int(os.path.getctime(curr_bag_path)))
            except Exception as e:
                logger.warning(f'{bag}: {e}')

    return record_time, upload_time


def get_database_csv_path(record_time):
    for k, v in DATA_TIME_FRAME.items():
        if date2timestamp(v[0]) <= record_time <= date2timestamp(v[1]):
            curr_csv_file = 'data_base_remote_' + k
            break
    else:
        curr_csv_file = 'data_base_remote_66ms_pc2'
    return os.path.join(CSV_PATH, f'{curr_csv_file}.csv')


def get_dst_path(record_time):
    for k, v in DATA_TIME_FRAME.items():
        if date2timestamp(v[0]) <= record_time <= date2timestamp(v[1]):
            curr_dst = f'{DST2}_{k}'
            break
    else:
        curr_dst = f'{DST2}_pc2'
    return os.path.join(CSV_PATH, curr_dst)


def data_copy(src_path, dst_path, filename):
    if SPECIFIC:
        curr_src_path = src_path
        curr_dst_path = dst_path
        record_time, upload_time = get_time(curr_src_path)
        recorded_data_path = get_database_csv_path(record_time)
    else:
        curr_src_path = os.path.join(src_path, filename)
        record_time, upload_time = get_time(curr_src_path)
        if dst_path == DST2:
            curr_dst_path = get_dst_path(record_time)
        else:
            curr_dst_path = dst_path
        recorded_data_path = get_database_csv_path(record_time)
        if int(time.time()) - upload_time < 3600 * HOUR:
            return

    ros_data_copy(curr_src_path, curr_dst_path, recorded_data_path)


def main():
    if SPECIFIC:
        data_copy(SRC0, DST0, os.path.basename(SRC0))
    else:
        for f in os.listdir(SRC1):
            data_copy(SRC1, DST1, f)

        for f in os.listdir(SRC2):
            data_copy(SRC2, DST1, f)

        for f in os.listdir(SRC3):
            if f == 'baoding_b06':  # TODO
                pass
                continue
            data_copy(SRC3, DST2, f)

    logger.info(f'copy finish')


if __name__ == '__main__':
    main()
