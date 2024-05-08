import os
import pandas as pd


def main(path):
    res = []
    columns = ['bag_name', 'radar_type', 'sequence', 'static', 'dynamic', 'valid_num']
    for r, d, f in os.walk(path):
        for _f in f:
            if _f == 'track_file.csv':
                _ = r.split('/')
                bag_name, radar_type = _[-2], _[-1]
                df = pd.read_csv(os.path.join(r, _f))
                df = df[df['valid_num'] >= 16]
                df['flg_all'] = df['flag_all'].apply(lambda x: int((x >> 8) & 3 != 0))
                for group, sub_df in df.groupby(['sequence']):
                    seq = group[0]
                    count_dict = sub_df['flg_all'].value_counts()
                    count_moving = count_dict.get(0, 0)
                    count_static = count_dict.get(1, 0)
                    valid_num = sub_df.shape[0]
                    res.append([bag_name, radar_type, seq, count_static, count_moving, valid_num])

    res = pd.DataFrame(data=res, columns=columns)
    res.to_csv('static_dynamic.csv', index=False)


if __name__ == '__main__':
    path = '/home/ztf/pythonProjects/helloworld/csv'
    main(path)
