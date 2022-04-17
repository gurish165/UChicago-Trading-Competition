'''
LSTM spot predictor for time-series data
Using Keras and Tensorflow

Input data:
Day of year since jan 1st 2016, rain for that month
TODO test out adding day of year to input
'''
from utils import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from metrics import evaluate
import pickle

print("started")

X_train, Y_train, X_test, Y_test = get_data()


print("data read in")


'''
plt.figure(figsize=(10,6)) #plotting

plt.plot(X_train[:,0],Y_train, label='2016-2019') #actual plot
plt.plot(X_test[:,0],Y_test, label='2020') #actual plot

#plt.plot(X_train, label='Actuall Data') #actual plot

plt.title('Time-Series Prediction')
plt.legend()
plt.show()
'''

resultsDict = {}
predictionsDict = {}


# For our dl model we will create windows of data that will be feeded into the datasets, for each timestemp T we will append the data from T-7 to T to the Xdata with target Y(t)
BATCH_SIZE = 64
BUFFER_SIZE = 100
WINDOW_LENGTH = 24


def window_data(X, Y, window=7):
    '''
    The dataset length will be reduced to guarante all samples have the window, so new length will be len(dataset)-window
    '''
    x = []
    y = []
    for i in range(window-1, len(X)):
        x.append(X[i-window+1:i+1])
        y.append(Y[i])
    return np.array(x), np.array(y)


# Since we are doing sliding, we need to join the datasets again of train and test
X_w = np.concatenate((X_train, X_test))
y_w = np.concatenate((Y_train, Y_test))

X_w, y_w = window_data(X_w, y_w, window=WINDOW_LENGTH)
X_train_w = X_w[:-len(X_test)]
y_train_w = y_w[:-len(X_test)]
X_test_w = X_w[-len(X_test):]
y_test_w = y_w[-len(X_test):]

# Check we will have same test set as in the previous models, make sure we didnt screw up on the windowing
print(f"Test set equal: {np.array_equal(y_test_w,Y_test)}")

train_data = tf.data.Dataset.from_tensor_slices((X_train_w, y_train_w))
train_data = train_data.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

val_data = tf.data.Dataset.from_tensor_slices((X_test_w, y_test_w))
val_data = val_data.batch(BATCH_SIZE).repeat()

dropout = 0
simple_lstm_model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(
        units=128, input_shape=X_train_w.shape[-2:], dropout=dropout, return_sequences = True),
    tf.keras.layers.LSTM(units=128),
    tf.keras.layers.Dense(128),
    tf.keras.layers.Dense(128),
    tf.keras.layers.Dense(1)
])

simple_lstm_model.compile(optimizer='rmsprop', loss='mae')


EVALUATION_INTERVAL = 200
EPOCHS = 5

model_history = simple_lstm_model.fit(train_data, epochs=EPOCHS,
                                      steps_per_epoch=EVALUATION_INTERVAL,
                                      validation_data=val_data, validation_steps=50)  # ,callbacks=[tensorboard_callback]) #Uncomment this

#yhat = simple_lstm_model.predict(X_test_w).reshape(1, -1)[0]
yhat = simple_lstm_model.predict(X_train_w).reshape(1, -1)[0]

#resultsDict['Tensorflow simple LSTM'] = evaluate(Y_test, yhat)
resultsDict['Tensorflow simple LSTM'] = evaluate(Y_train, yhat)

predictionsDict['Tensorflow simple LSTM'] = yhat

with open('results/scores_train.pickle', 'wb') as handle:
    pickle.dump(resultsDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('results/predictions_train.pickle', 'wb') as handle:
    pickle.dump(predictionsDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
