import geopandas
from osgeo import gdal, gdal_array
import numpy as np

traceResult={}
polluting= geopandas.read_file('../Data/geoJson/pollution.geojson')

raster="../resultData/computingResult/TN_experience_formula.tif"
srcArray = gdal_array.LoadFile(raster)

srcArray[np.isnan(srcArray)]=-999

n=10
maxten=[]
maxtenposition=[]
for i in range(n):
    bm = np.nanmax(srcArray)
    pos = np.unravel_index(np.argmax(srcArray), srcArray.shape)
    maxten.append(bm)
    maxtenposition.append(pos)
    srcArray[pos[0],pos[1]]=-999

dataset = gdal.Open(raster)

adfGeoTransform = dataset.GetGeoTransform()


nXSize = dataset.RasterXSize #列数
nYSize = dataset.RasterYSize #行数

arrSlope = [] # 用于存储每个像素的（X，Y）坐标

i=0
polluting_list=[]
for i in range(polluting.shape[0]):
    polluting_list.append([])
    polluting_list[-1].append(i+1)
    polluting_list[-1].append(polluting.iat[i,1])
    polluting_list[-1].append(polluting.iat[i,-1].x)
    polluting_list[-1].append(polluting.iat[i,-1].y)


i=0
for i in range(len(maxtenposition)):
    num=maxtenposition[i]
    x=num[0]
    y=num[1]
    px = adfGeoTransform[0] + y * adfGeoTransform[1] + x * adfGeoTransform[2]
    py = adfGeoTransform[3] + y * adfGeoTransform[4] + x * adfGeoTransform[5]

    distance_list=[]
    for m in polluting_list:
        dis=pow((m[2]-px),2)+pow((m[3]-py),2)
        distance_list.append(dis)

    id=distance_list.index(min(distance_list))+1
    traceResult[id]=0

print(traceResult.keys())






