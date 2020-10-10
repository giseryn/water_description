import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from sklearn.model_selection import train_test_split
import joblib
from osgeo import gdal


def try_different_method(model, model_name):
    model_filename = model_name + '.model'
    model.fit(x_train, y_train)
    joblib.dump(filename="../resultData/machineLearningModel/" + model_filename, value=model)
    score = model.score(x_test, y_test)
    result = model.predict(x_test)
    print(len(result))
    for i in range(len(result)):
        sum_result = (y_test[i] - result[i]) * (y_test[i] - result[i])
    mse_number = sum_result / len(result)
    print(mse_number)
    rmse_number = math.sqrt(mse_number)
    print(rmse_number)

    plt.figure()
    plt.plot(np.arange(len(result)), y_test, 'go-', label='true value')
    plt.plot(np.arange(len(result)), result, 'ro-', label='predict value')

    plt.title('score: %f' % score + ' ' + 'rmse_number: %f' % rmse_number)

    plt.legend()
    plt.show()


def runModel(X):
    out = SVM.predict(X);
    return out


if __name__ == '__main__':

    file_name = "../resultData/trainData/data_train.csv"
    data_train = pd.read_csv(file_name, encoding='gbk', )

    X = data_train[['Blue', 'Green', 'Red', 'Near infrared']]
    y = data_train[['chlorophyll']]
    x_train, x_test, y_train, y_test = train_test_split(X, y.values.ravel(), test_size=0.3)

    from sklearn import svm

    model_SVR = svm.SVR(C=100, kernel='poly', degree=5)
    try_different_method(model_SVR,'supportVectorProductModel')

    SVM=joblib.load("../resultData/machineLearningModel/supportVectorProductModel.model")

    print(SVM)
    dataset = gdal.Open("../Data/tif/deqingwater.tif", gdal.GA_ReadOnly)
    cols = dataset.RasterXSize  # 图像长度
    rows = dataset.RasterYSize  # 图像宽度
    bands = []
    for i in range(dataset.RasterCount):
        num = i + 1
        select_band = dataset.GetRasterBand(num)
        band = select_band.ReadAsArray(0, 0, cols, rows)
        bands.append(band)
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)
    new_tiff_name = '../resultData/computingResult/supportVectorProductModel.tif'
    outDataset = driver.Create(new_tiff_name, cols, rows, 1, gdal.GDT_Float32)

    geoTransform = dataset.GetGeoTransform()
    outDataset.SetGeoTransform(geoTransform)
    proj = dataset.GetProjection()
    outDataset.SetProjection(proj)

    data = []
    for m in range(rows):
        data.append([])
        if m % 100 == 0:
            print(str(m) + "/" + str(rows))
        for n in range(cols):
            if bands[0][m][n] != 0:
                train_data = [bands[0][m][n], bands[1][m][n], bands[2][m][n], bands[3][m][n]]
                train_data = np.asarray(train_data)
                train_data = train_data.reshape(1, -1)
                svmresult = runModel(train_data)
                data[-1].append(svmresult)
            else:
                svmresult = np.nan
                data[-1].append(svmresult)

    outBand = outDataset.GetRasterBand(1)
    data_array = np.asarray(data)
    outBand.WriteArray(data_array, 0, 0)
