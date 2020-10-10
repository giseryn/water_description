import os
from osgeo import gdal
import time
import os,sys


def tiff_tailor(tiff_data_dir, tiff_name):
    input_shape = "../Data/shp/deqing.shp"
    input_raster = tiff_data_dir + "/" + tiff_name
    print(os.getcwd())
    output_raster = "../resultData/tailorResult/result_" + tiff_name
    print(input_raster,output_raster)
    # tif输入路径，打开文件

    # 矢量文件路径，打开矢量文件
    input_raster = gdal.Open(input_raster)
    ds = gdal.Warp(output_raster,
                   input_raster,
                   format='GTiff',
                   cutlineDSName=input_shape,
                   cutlineWhere="FIELD = 'whatever'",
                   dstNodata=0)
    # 关闭文件
    ds = None


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
        return files

def RasterMosaic(inputfilePath,referencefilefilePath,outputfilePath):
    print("图像拼接")
    print(inputfilePath,referencefilefilePath,outputfilePath)
    inputrasfile1 = gdal.Open(inputfilePath, gdal.GA_ReadOnly) # 第一幅影像
    inputProj1 = inputrasfile1.GetProjection()
    inputrasfile2 = gdal.Open(referencefilefilePath, gdal.GA_ReadOnly) # 第二幅影像

    options=gdal.WarpOptions(srcSRS=inputProj1, dstSRS=inputProj1,format='GTiff')
    gdal.Warp(outputfilePath,[inputrasfile1,inputrasfile2],options=options)

if __name__ == '__main__':

    time_start = time.time()

    tiff_fill_dir = "../Data/GF1"
    tiff_files_name = file_name(tiff_fill_dir)
    for i in tiff_files_name:
        tiff_tailor(tiff_fill_dir, i)

    tiff_mosaic_file="tailor_result"
    mosaic_files_name = file_name("../resultData/tailorResult")
    outputfilePath1 = '../resultData/mosaicResult/test_tiff1.tif'
    outputfilePath2 = '../resultData/mosaicResult/test_tiff2.tif'
    outputfilePath3 = '../resultData/mosaicResult/test_tiff3.tif'
    for m in range(len(mosaic_files_name)):
        mosaic_files_name[m]="../resultData/tailorResult/"+mosaic_files_name[m]

    RasterMosaic(mosaic_files_name[0],mosaic_files_name[1],outputfilePath1)
    RasterMosaic(mosaic_files_name[2],mosaic_files_name[3],outputfilePath2)
    RasterMosaic(outputfilePath1, outputfilePath2,outputfilePath3)

    time_end = time.time()
    print('totally cost', time_end - time_start)










