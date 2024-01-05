import os
import re
import csv
import time
import rosbag
import pandas as pd
from subprocess import Popen, PIPE
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Queue

path = '/home/ztf/nas/CornerRadarDatabase'
# path = '/home/ztf/nas/01_测试数据/05_2944前角雷达/03_功能需求数据/FCTA'

duration = dict()
with open('time.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
    for i in data[1:]:
        if i[0] == '':
            break
        duration[i[0]] = [i[1], i[2]]


result_q = {k: Queue(10) for k in duration}
pattern_duration = re.compile(r'duration:.*?\((\d+)s\)')
pattern_size = re.compile(r'size:.*?(\d.*?GB)')


def get_size_duration(filename, path, q, count):
    try:
        # print(f'bag{count} start')
        # cmd = f'rosbag info {path}'
        # start = time.time()
        # resp = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # stdout, stderr = resp.communicate()
        # pattern_str = stdout.decode()
        #
        # curr_duration = re.findall(pattern_duration, pattern_str)[0]
        # curr_bag_size = re.findall(pattern_size, pattern_str)[0]
        # curr_row = [finename, path, curr_duration, curr_bag_size]

        # print(f'start read {path}')
        # start = time.time()
        # curr_bag = rosbag.Bag(path)
        # print(f'{filename} duration is {round(curr_bag.get_end_time() - curr_bag.get_start_time(), 2)}s, read bag cost time {time.time() - start}')

        curr_bag_size = f'{round(os.path.getsize(path) / 1024 / 1024 / 1024, 2)}GB'
        curr_row = [filename, path.replace('/home/ztf', ''), curr_bag_size]

        q.put(curr_row)
        # print(f'bag{count} finish, duration: {curr_duration}, size: {curr_bag_size}, cost time {time.time() - start}')
    except Exception as e:
        print(e)


def get_final_res(q, k):
    result = []
    while True:
        res = q.get()
        if res is None:
            break
        result.append(res)

    # print(result)
    # result = pd.DataFrame(result, columns=['bag_path', 'bag_name', 'bag_duration', 'bag_size'])
    result = pd.DataFrame(result, columns=['bag_name', 'bag_path', 'bag_size'])
    result['time'] = result['bag_name'].apply(lambda x: ''.join(x.replace('.bag', '').replace('-', '_').split('_')[2: -1]))
    result['vehicle_type'] = result['bag_name'].apply(lambda x: '_'.join(x.replace('.bag', '').replace('-', '_').split('_')[:2]))
    result = result.sort_values(by='time')
    result = result[['bag_path', 'bag_name', 'bag_size', 'vehicle_type']]
    # result = result[['bag_path', 'bag_name', 'bag_size', 'bag_duration', 'vehicle_type']]
    result.to_csv(f'{k}.csv', index=None)


def main():
    plist = []
    for k in result_q:
        p = Process(target=get_final_res, args=(result_q[k], k))
        plist.append(p)
        p.start()

    futures = []
    count = 0
    ignore_folders = ['标准场景_66ms', '标准场景_88ms', '标准场景_pc2', 'autosar数据', 'B01G_data', 'backup', 'Static_target_scene', '00_数据统计', '']
    with ThreadPoolExecutor(max_workers=10) as executor:
        for root, dirs, files in os.walk(path):
            curr_root = root.replace(path, '')
            curr_folder = curr_root.split('/')[1] if curr_root else ''
            if curr_folder in ignore_folders:
                continue
            # if count == 5:
            #     break
            for f in files:
                if f.endswith('.bag'):
                    count += 1
                    # if count == 5:
                    #     break
                    curr_full_path = os.path.join(root, f)
                    bag_time = ''.join(f.replace('.bag', '').replace('-', '_').split('_')[2: -1])
                    for data_type in duration:
                        if duration[data_type][0] <= bag_time <= duration[data_type][1]:
                            futures.append(executor.submit(get_size_duration, f, curr_full_path, result_q[data_type], count))
                            break

        for f in futures:
            _ = f.result()

    for k in result_q:
        result_q[k].put(None)

    for p in plist:
        p.join()


if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
