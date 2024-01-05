def set_pandas_option():
    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 不换行显示
    pd.set_option('display.width', 1000)


def get_logger():
    import logging
    lg = logging.getLogger()
    lg.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s-line%(lineno)d-%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    lg.addHandler(console_handler)
    return lg


def date2timestamp(date, fmt="%Y-%m-%d-%H-%M-%S"):
    import time
    from datetime import datetime
    dt = datetime.strptime(date, fmt)
    return int(time.mktime(dt.timetuple()))


def read_rosbag(bag_path):
    import rosbag
    data = rosbag.Bag(bag_path)
    duration = str(int(data.get_end_time() - data.get_start_time()))
    return duration


def use_popen():
    from subprocess import Popen, PIPE
    bag_path = '/home/ztf/nas/CornerRadarDatabase/20231109_TC_2944_4radar_changgui_v3.1.6_crc1323_tuan_caofolin/V8.0.3_track_6g_0.51_fusion_6g_0.51_changui_tuan_02/rosbag/tuan_ETC882_2023-11-09-14-36-45_0.bag'
    cmd = f'rosbag info {bag_path}'
    resp = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = resp.communicate()

    with open('xxx', 'w') as f:
        f.write(stderr.decode())
        f.write(stdout.decode())


def django_cmd():
    '''
    python manage.py inspectdb > web/models.py  数据库文件转成models文件
    :return:
    '''
    pass