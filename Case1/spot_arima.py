# fit an ARIMA model and plot residual errors
from pandas import datetime
from pandas import read_csv
from pandas import DataFrame
from pandas.plotting import lag_plot
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np
from utils import get_data
from sklearn.metrics import mean_squared_error
import glob
import pandas as pd



#X_train, Y_train, X_test, Y_test = get_data()
# load dataset
#dayOfYear = range(Y_train.shape[0])

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

prices_20 = pd.read_csv('./prices_2020.csv')
rain_20 = pd.read_csv('./rain_2020.csv')

'''
plt.figure()
lag_plot(prices_train.iloc[:,1], lag=3)
plt.title('Autocorrelation plot with lag = 3')
plt.show()
'''


training_data = prices_train.iloc[:,1].values

test_data = prices_20.iloc[:,1].values

history = [x for x in training_data]
model_predictions = []
N_test_observations = len(test_data)

# fit model
for time_point in range(N_test_observations):
    model = ARIMA(history, order=(4,1,0))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    model_predictions.append(yhat)
    true_test_value = test_data[time_point]
    history.append(true_test_value)
MSE_error = mean_squared_error(test_data, model_predictions)
print('Testing Mean Squared Error is {}'.format(MSE_error))

plt.figure(figsize=(10,6)) #plotting

#plt.plot(X_train[:,0],Y_train, label='2016-2019') #actual plot
plt.plot(test_data, label='actual') #actual plot
plt.plot(model_predictions, label='pred')

plt.title('Time-Series Prediction')
plt.legend()
plt.show()

