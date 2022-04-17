'''
Utils for case1
Data handeling etc
'''
import pandas as pd
import glob
import numpy as np



def get_data():
    '''
    return X_train, Y_train
    '''
    # training data years 2016-2019
    train_prices_path = glob.glob("./prices_201*.csv")
    train_rain_path = glob.glob("./rain_201*.csv")

    # read in data
    prices_train = pd.DataFrame()
    rain_train = pd.DataFrame()

    for f in train_prices_path:
        csv = pd.read_csv(f)
        prices_train = pd.concat([prices_train, csv])
    for f in train_rain_path:
        csv = pd.read_csv(f)
        rain_train = pd.concat([rain_train, csv])

    # precipitation for the month that each day is in
    precip = []
    # day since begging of training data
    dayOfYear = range(prices_train.shape[0])

    for p in rain_train.iloc[:,1]:
        for i in range(21): # 21 trading days per month
            precip.append(p)

    X_train = np.column_stack((dayOfYear, precip)).astype(float)
    Y_train = np.array(prices_train.iloc[:,1]).astype(float)

    prices_20 = pd.read_csv('./prices_2020.csv')
    rain_20 = pd.read_csv('./rain_2020.csv')

    testDayOfYear = range(dayOfYear[len(dayOfYear)-1], dayOfYear[len(dayOfYear)-1] + prices_20.shape[0])
    test_precip = []

    for p in rain_20.iloc[:,1]:
        for i in range(21):
            test_precip.append(p)

    X_test = np.column_stack((testDayOfYear, test_precip)).astype(float)
    Y_test = np.array(prices_20.iloc[:,1]).astype(float)

    return X_train, Y_train, X_test, Y_test