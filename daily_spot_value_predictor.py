from sklearn import svm
import sklearn as sk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in data
prices_16 = pd.read_csv('prices_2016.csv')
rain_16 = pd.read_csv('rain_2016.csv')

prices_17 = pd.read_csv('prices_2017.csv')
rain_17 = pd.read_csv('rain_2017.csv')


# input is day of year, precip of that month
# set up input and ouput


dayOfYear = range(252)
precip = [] # precipitation for the month that each day is in

for p in rain_16.iloc[:,1]:
    for i in range(21):
        precip.append(p)



X = np.column_stack((dayOfYear, precip))
y = prices_16.iloc[:,1]

# set up model and fit data to model
regr = sk.svm.SVR(kernel='rbf')
regr.fit(X, y)


# test output
precip_17 = []
for p in rain_17.iloc[:,1]:
    for i in range(21):
        precip_17.append(p)


test = np.column_stack((dayOfYear, precip_17))
out = regr.predict(test)
#print("Test Output:",out)

plt.plot(dayOfYear,prices_17.iloc[:,1])
plt.plot(dayOfYear,out)

#plt.set_label("Ground Truth", "Predict")
plt.show()