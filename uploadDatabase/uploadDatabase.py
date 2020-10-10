import geopandas
import pandas as pd
import psycopg2
import time

def load_data_to_pg(file_name,table_name):
    # 根据id确定监测站地理坐标
    json_data = geopandas.read_file('../Data/geoJson/monitor-point.geojson')
    monitor_point = pd.DataFrame(json_data)

    data_624 = pd.read_csv(file_name, encoding='gbk')
    data_624 = data_624.dropna()

    result = pd.merge(data_624, monitor_point, on='id')

    conn = psycopg2.connect(database="deqing", user="postgres", password="123456", host="123.57.77.224", port="5432")
    print("Opened database successfully")

    cur = conn.cursor()

    cur.execute('''CREATE TABLE table_name
                       (ID INT PRIMARY KEY     NOT NULL,
                       NAME           text    NOT NULL,
                       date           text ,
                       chlorophyll    float,
                    dissolved_oxygen  float,
                       TP             float,
                       lng            float,
                       lat            float );''')
    print("Table created successfully")

    for i in range(result.shape[0]):
        NAME = result.iat[i, 1]
        date = result.iat[i, 2]
        date2 = str(date)
        datearray = time.strptime(date, "%Y/%m/%d")

        chlorophyll = result.iat[i, 3]
        dissolved_oxygen = result.iat[i, 4]
        TP = result.iat[i, 5]
        location = result.iat[i, 6]
        lng = location.x
        lat = location.y

        cur.execute(f"INSERT INTO table_name (ID, NAME, date , chlorophyll, dissolved_oxygen,TP,lng,lat ) "
                    f"VALUES ({++i}, '{NAME}', '{date2}', '{chlorophyll}', '{dissolved_oxygen} ','{TP}','{lng}','{lat}')")

    new_name =table_name
    db_word = "alter table table_name rename to " + new_name
    cur.execute(db_word)
    conn.commit()

if __name__ == '__main__':

    file_name="../Data/csv/6-24模拟监测站数据.csv"
    table_name="June_24th"
    load_data_to_pg(file_name,table_name)

    file_name = "../Data/csv/7-24模拟监测站数据.csv"
    table_name = "July_24th"
    load_data_to_pg(file_name, table_name)

    file_name = "../Data/csv/8-24模拟监测站数据.csv"
    table_name = "Augest_24th"
    load_data_to_pg(file_name, table_name)
