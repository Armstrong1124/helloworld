import sqlite3
import pandas as pd

path = './database/data_base_remote_66ms.csv'

df = pd.read_csv(path)
# df = pd.DataFrame(data=[['ztf', 18]], columns=['name', 'age'])

conn = sqlite3.connect('test.db3')

drop_table_sql = '''
DROP TABLE IF EXISTS mytable
'''
create_table_sql = '''
CREATE TABLE mytable(
car CHAR(20),
path CHAR(20),
bag CHAR(20),
bag_duration CHAR(20),
scene_names CHAR(20),
scene_types CHAR(20),
road_types CHAR(20),
vehicle_types CHAR(20),
autopilot_status CHAR(20),
side_status CHAR(20),
tunnel_status CHAR(20),
weather_status CHAR(20)
)
'''
query_data_type = '''
PRAGMA table_info(my_table)
'''
conn.execute(drop_table_sql)
conn.execute(create_table_sql)
df = df.astype(str)
df.to_sql('mytable', conn, if_exists='replace', index=False)

conn.close()
