'''
read in pickle files and show predictions
'''
from utils import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

X_train, Y_train, X_test, Y_test = get_data()

objects_train = []
with (open("results/predictions_train.pickle", "rb")) as openfile:
    while True:
        try:
            objects_train.append(pickle.load(openfile))
        except EOFError:
            break

objects_test = []
with (open("results/predictions.pickle", "rb")) as openfile:
    while True:
        try:
            objects_test.append(pickle.load(openfile))
        except EOFError:
            break

predictions = objects_train[0]['Tensorflow simple LSTM']
predictions_test = objects_test[0]['Tensorflow simple LSTM']

print(predictions.size)

plt.figure(figsize=(10,6)) #plotting

#plt.plot(X_train[:,0],Y_train, label='2016-2019') #actual plot
plt.plot(X_train[:,0],Y_train, label='train') #actual plot
plt.plot(X_train[:985,0],predictions, label='train fit') #actual plot

plt.plot(X_test[:,0],Y_test, label='test') #actual plot
plt.plot(X_test[:,0],predictions_test, label='test fit') #actual plot


#plt.plot(X_train, label='Actuall Data') #actual plot

plt.title('Time-Series Prediction')
plt.legend()
plt.show()