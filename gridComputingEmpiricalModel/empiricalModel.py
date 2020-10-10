from osgeo import gdal

def get_band(file_name):
    global dataset
    global cols
    global rows
    dataset = gdal.Open(file_name)
    print(dataset.GetDescription())  # 数据描述

    print(dataset.RasterCount)  # 波段数

    cols = dataset.RasterXSize  # 图像长度
    rows = dataset.RasterYSize  # 图像宽度

    xoffset = cols / 2
    yoffset = rows / 2
    print("xoffset:", xoffset)
    print("yoffset:", yoffset)

    band = dataset.GetRasterBand(1)
    b1 = band.ReadAsArray(0, 0, cols, rows)

    band = dataset.GetRasterBand(2)
    b2 = band.ReadAsArray(0, 0, cols, rows)

    band = dataset.GetRasterBand(3)
    b3 = band.ReadAsArray(0, 0, cols, rows)

    band = dataset.GetRasterBand(4)
    b4 = band.ReadAsArray(0, 0, cols, rows)
    return b1, b2, b3, b4

def set_property(outDataset):
    # 同步基准面与坐标
    geoTransform = dataset.GetGeoTransform()
    outDataset.SetGeoTransform(geoTransform)
    proj = dataset.GetProjection()
    outDataset.SetProjection(proj)

    # 输出栅格波段
    outBand = outDataset.GetRasterBand(1)

    ND = dataset.GetRasterBand(1).GetNoDataValue()
    outBand.SetNoDataValue(ND)
    return outBand


def Chla(b3,b4):
    global Chla_data
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)

    output_name="../resultData/computingResult/Chla_experience_formula.tif"
    outDataset = driver.Create(output_name, cols, rows, 1, gdal.GDT_Float32)
    outBand=set_property(outDataset)

    Chla_data = 4.089 * pow((b4 / b3), 2) - 0.746 / (b4 / b3) + 29.7311
    outBand.WriteArray(Chla_data, 0, 0)

def TSS(b2,b3):
    global TSS_data
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)

    output_name="../resultData/computingResult/TSS_experience_formula.tif"
    outDataset = driver.Create(output_name, cols, rows, 1, gdal.GDT_Float32)
    outBand=set_property(outDataset)

    TSS_data= 119.62*pow((b3/b2),6.0823)
    outBand.WriteArray(TSS_data, 0, 0)

def Zsd():
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)

    output_name="../resultData/computingResult/Zsd_experience_formula.tif"
    outDataset = driver.Create(output_name, cols, rows, 1, gdal.GDT_Float32)
    outBand=set_property(outDataset)

    Zsd_data= 284.15*pow(TSS_data,-0.67)
    outBand.WriteArray(Zsd_data, 0, 0)

def TP():
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)

    output_name="../resultData/computingResult/TP_experience_formula.tif"
    outDataset = driver.Create(output_name, cols, rows, 1, gdal.GDT_Float32)
    outBand=set_property(outDataset)

    TP_data= -0.00078*Chla_data+0.0417
    outBand.WriteArray(TP_data, 0, 0)

def TN():
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)

    output_name="../resultData/computingResult/TN_experience_formula.tif"
    outDataset = driver.Create(output_name, cols, rows, 1, gdal.GDT_Float32)
    outBand=set_property(outDataset)

    TN_data= 3.166-0.03479*Chla_data
    outBand.WriteArray(TN_data, 0, 0)

def CODMN():
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)

    output_name="../resultData/computingResult/CODMN_experience_formula.tif"
    outDataset = driver.Create(output_name, cols, rows, 1, gdal.GDT_Float32)
    outBand=set_property(outDataset)

    CODMN_data= 0.05*Chla_data+4.543
    outBand.WriteArray(CODMN_data, 0, 0)



if __name__ == '__main__':
    file_name = "../Data/tif/deqingwater.tif"
    b1, b2, b3, b4=get_band(file_name)

    Chla(b3,b4)
    TSS(b2, b3)
    Zsd()
    TP()
    TN()
    CODMN()








