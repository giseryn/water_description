import psycopg2
from osgeo import gdal, gdal_array
import shapefile
from pandas.core.frame import DataFrame

def get_point_pixel_value(table_name):
    conn = psycopg2.connect(database="deqing", user="postgres", password="123456", host="123.57.77.224", port="5432")
    print("Opened database successfully")

    cur = conn.cursor()
    db_word="SELECT ID, NAME, date , chlorophyll, dissolved_oxygen,TP,lng,lat from "+table_name
    cur.execute(db_word)
    rows = cur.fetchall()
    for i in rows:
        print(i[0])
        lng=i[-2]
        lat=i[-1]
        world2pixel(geoTrans,lng,lat,i[0])
        monitor_point[-1].append(i[3])
        monitor_point[-1].append(i[4])
        monitor_point[-1].append(i[5])
    print("Operation done successfully");
    conn.close()

def world2pixel(geoMatrix, x, y,id):
    """
    使用gdal库的geomatrix对象(gdal.GetGeoTransform())计算地理坐标的像素位置
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / abs(yDist))

    monitor_point.append([])
    monitor_point[-1].append(id)
    monitor_point[-1].append(srcArray[0][pixel][line])
    monitor_point[-1].append(srcArray[1][pixel][line])
    monitor_point[-1].append(srcArray[2][pixel][line])
    monitor_point[-1].append(srcArray[3][pixel][line])


if __name__ == '__main__':
    raster = "../Data/tif/deqing.tif"

    srcArray = gdal_array.LoadFile(raster)
    srcImage = gdal.Open(raster)
    geoTrans = srcImage.GetGeoTransform()
    monitor_point=[]

    table_name="june_24th"
    get_point_pixel_value(table_name)

    data_train = DataFrame(monitor_point,
                           columns=['ID', 'Blue', 'Green', 'Red', 'Near infrared', 'chlorophyll', 'dissolved_oxygen',
                                    'total_phosphorus'])

    data_train.to_csv("../resultData/trainData/data_train.csv",header=True,index=False)













