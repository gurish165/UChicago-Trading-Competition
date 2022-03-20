import sklearn as sk
import pandas as pd
import numpy as np

# read in data
prices_16 = pd.read_csv('prices_2016.csv')
rain_16 = pd.read_csv('rain_2016.csv')

# input is day of year, precip of that month
# set up input and ouput


dayOfYear = range(251)
precip = [] # precipitation for the month that each day is in

for p in rain_16.iloc[:,1]:
    for i in range(21):
        precip.append(p)



X = np.column_stack(dayOfYear, precip)
y = prices_16.iloc[:,1]

# set up model and fit data to model
regr = sk.svm.SVR()
regr.fit(X, y)


# test output
test = []
print("Test Output:",regr.predict(test))
