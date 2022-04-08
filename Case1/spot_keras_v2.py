'''
https://towardsdatascience.com/lstm-time-series-forecasting-predicting-stock-prices-using-an-lstm-model-6223e9644a2f
'''
import math
import matplotlib.pyplot as plt
import keras
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from utils import get_data
import pickle
import glob

#X_train, Y_train, X_test, Y_test = get_data()

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

prices_20 = pd.read_csv('./prices_2020.csv')
rain_20 = pd.read_csv('./rain_2020.csv')

testDayOfYear = range(dayOfYear[len(dayOfYear)-1]+1, 1 + dayOfYear[len(dayOfYear)-1] + prices_20.shape[0])
test_precip = []

for p in rain_20.iloc[:,1]:
    for i in range(21):
        test_precip.append(p)


train = prices_train
train['precip'] = precip
train['timestamp'] = dayOfYear

test = prices_20
test['precip'] = test_precip
test['timestamp'] = testDayOfYear

#print(train)
#print(test)

training_set = train[['timestamp', 'precip', 'Daily Price']].values
training_set_df = train[['timestamp', 'precip', 'Daily Price']].copy()

test_set = test[['timestamp', 'precip', 'Daily Price']].values
test_set_df = test[['timestamp', 'precip', 'Daily Price']].copy()


#print(training_set[1:10])
#print(test_set)
#print(test_set.shape)



## Make data windows that feed into models

# Feature Scaling
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

#print(training_set_scaled[1:10])


window_size = 60
# Creating a data structure with 60 time-steps and 1 output
X_train = []
y_train = []
for i in range(window_size, training_set_scaled.shape[0]):
    X_train.append(training_set_scaled[i-window_size:i, 0:2])
    y_train.append(training_set_scaled[i, 2])
    #print(training_set_scaled[i-window_size:i, 0].size)
    #print(training_set_scaled[i-window_size:i, 0:2])
    #print(training_set_scaled[i, 2])
X_train, y_train = np.array(X_train), np.array(y_train)
#X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1)) # not needed

#print(X_train.shape)
#(987, 21, 2)
#print(y_train.shape)
#(987,)

#test_set
#print(test_set)
#print(test_set.shape)

#test_set = test_set.reshape(-1,1)
#print(test_set)
#print(test_set.shape)

# Initialising the RNN and train the model

model = Sequential()
#Adding the first LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 2)))
model.add(Dropout(0.2))
# Adding a second LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))
# Adding a third LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))
# Adding a fourth LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50))
model.add(Dropout(0.2))
# Adding the output layer
model.add(Dense(units = 1))

# Compiling the RNN
model.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
model.fit(X_train, y_train, epochs = 10, batch_size = 32)

# Predictions

test_set = sc.transform(test_set)
X_test = []
for i in range(window_size, test_set.shape[0]):
    X_test.append(test_set[i-window_size:i, 0:2])

X_test = np.array(X_test)

#print(X_test.shape)
#(231, 21, 2)

#predicted_stock_price = model.predict(X_test)
predicted_stock_price_train = model.predict(X_train)


#print(predicted_stock_price.shape)
#print(predicted_stock_price)

# configure shape of output so that we can inverse it
#predicted_stock_price = predicted_stock_price.reshape(predicted_stock_price.shape[0])

predicted_stock_price = np.hstack((test_set[window_size:,0:2], predicted_stock_price))

predicted_stock_price_train = np.hstack((training_set[window_size:,0:2], predicted_stock_price_train))

#predicted_stock_price = np.pad(predicted_stock_price, )


#print(predicted_stock_price.shape)
#print(test_set[window_size:,0:2].shape)
#print(test_set[window_size:,0:2])

#print(test_set.shape)
#(252, 3)

#print(predicted_stock_price[1:10])

predicted_stock_price = sc.inverse_transform(predicted_stock_price)

predicted_stock_price_train = sc.inverse_transform(predicted_stock_price_train)

#print(predicted_stock_price)

# Visualising the results
plt.figure(figsize=(10,6)) #plotting

#plt.plot(X_train[:,0],Y_train, label='2016-2019') #actual plot
#plt.plot(predicted_stock_price[:,2], label='pred') #actual plot
#plt.plot(test_set_df.iloc[:,2], label='actual') #actual plot
plt.plot(training_set_df.iloc[:,2], label='pred') #actual plot
plt.plot(predicted_stock_price_train[:,2], label='pred') #actual plot





plt.title('Time-Series Prediction')
plt.legend()
plt.show()


