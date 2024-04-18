import os.path
import time

def set_pandas_option():
    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 不换行显示
    pd.set_option('display.width', 1000)


def some_useful_func_import_from():
    from functools import partial
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    from collections import defaultdict, namedtuple, OrderedDict
    pass


def time_cost(logger):
    def _time_cost(func):
        def __time_cost(*args):
            start = time.time()
            func(*args)
            logger.info(f'{func.__name__} time cost {time.time() - start}s')
        return __time_cost
    return _time_cost



def get_logger():
    import os
    import logging
    from logging.handlers import TimedRotatingFileHandler
    from datetime import datetime
    lg = logging.getLogger()
    lg.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s-line%(lineno)d-%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    lg.addHandler(console_handler)

    now = datetime.now()
    now = now.strftime('%Y-%m-%d-%H-%M-%S')
    os.makedirs('log', exist_ok=True)
    file_handler = logging.FileHandler(f'log/{now}.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    lg.addHandler(file_handler)
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


def coordinate_transformation1(x, y):
    import numpy as np
    x = np.mat(x)
    y = np.mat(y)
    center_x = np.mean(x, axis=0)
    center_y = np.mean(y, axis=0)
    re_x = x - center_x
    re_y = y - center_y
    h = re_x.T*re_y
    u, s, vt = np.linalg.svd(h)
    r = vt.T*u.T
    if np.linalg.det(r) < 0:
        vt[2, :] *= -1
        r = vt.T*u.T
    t = -r*center_x.T + center_y.T
    return r, t


def coordinate_transformation2(x, y):
    import numpy as np
    x = np.mat(x)
    y = np.mat(y)
    center_x = np.mean(x, axis=0)
    center_y = np.mean(y, axis=0)
    re_x = x - center_x
    re_y = y - center_y
    r = np.linalg.inv(re_x.T*re_x)*re_x.T*re_y
    t = -r*center_x.T + center_y.T
    return r, t


def sql_insert_del_update_select():
    from sqlalchemy import create_engine, MetaData
    from sqlalchemy.orm import sessionmaker
    import pandas as pd
    engine = create_engine('mysql+pymysql://radar_data:123@10.44.23.121:3306/test')
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    curr_table = metadata.tables['data_base_remote_66ms_pc2']
    res = session.query(curr_table).filter(curr_table.c.autopilot_status == '12').update({'scene_types': '777'})
    session.commit()
    session.close()
    sql = 'SELECT * FROM test.data_base_remote_66ms_pc2;'
    data = pd.read_sql(sql, engine)