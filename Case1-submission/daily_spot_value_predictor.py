from typing import ClassVar
from sklearn import svm
import sklearn as sk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob 

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
# prices_train = pd.read_csv('prices_201*.csv')
# rain_train = pd.read_csv('rain_201*.csv')

prices_20 = pd.read_csv('prices_2020.csv')
rain_20 = pd.read_csv('rain_2020.csv')


# input is day of year, precip of that month
# set up input and ouput

# print(rain_train.shape)
dayOfYear = range(prices_train.shape[0])
precip = [] # precipitation for the month that each day is in

for p in rain_train.iloc[:,1]:
    for i in range(21):
        precip.append(p)


X = np.column_stack((dayOfYear, precip)).astype(float)
# print(X)
y = np.array(prices_train.iloc[:,1]).astype(float)
# print(y)

# set up model and fit data to model
def cross_validation_performance(model, X, y, k=5):
    scores = []
    skf = sk.model_selection.KFold(n_splits=k)
    for train_index ,val_index in skf.split(X,y):
        X_cv_train, X_cv_val = X[train_index], X[val_index]
        y_cv_train, y_cv_val = y[train_index], y[val_index]
        # print(type(X_cv_train))
        model.fit(X_cv_train, y_cv_train)
        y_cv_predicted = model.predict(X_cv_val)
        scores.append(sk.metrics.accuracy_score(y_cv_val, y_cv_predicted))
    return np.array(scores).mean()

def SVR_hyperparameter_selection(X, y, k=5, C_range=[], kernels=['poly', 'rbf', 'rbf#0.01', 'rbf#0.1', 'rbf#1', 'rbf#10', 'rbf#100', 'sigmoid']):
    performance_matrix = []
    gamma = ''
    for kernel in kernels:
        kernel_performance_list = []
        for c_value in C_range:
            sp = kernel.split('#')
            kernel = sp[0]
            gamma = 'scale'
            if len(sp)==2:
                gamma = sp[1].astype(float)
            regr = svm.SVR(kernel=kernel, gamma=gamma, C=c_value, verbose=False)
            kernel_performance_list.append(cross_validation_performance(regr, X, y, k))
            print("Kernel: ", kernel)
            print("C_value: ", c_value)
        performance_matrix.append(kernel_performance_list)
    best_index = np.argmax(performance_matrix, axis=None)
    print("Best Index: ", best_index)
    best_kernel = best_index // len(C_range)
    best_C = best_index % len(kernels)
    return kernels[best_kernel], C_range[best_C]

# C_range = [np.random.uniform(-2,2,10)]
# C_range = [10*c_val for c_val in C_range] # 10 real numbers from 0.01 to 100
# best_kernel, best_C = SVR_hyperparameter_selection(X, y, C_range=C_range)
# print("The Best Kernel: ", best_kernel)
# print("The Best C Value", best_C)
# gamma='scale'
# sp = best_kernel.split('#')
# best_kernel = sp[0]
# if len(sp)==2:
#     gamma = float(sp[1])
SVR_model = svm.SVR(kernel='rbf',gamma=0.0079, C=500)
# one of the best one: kernel='rbf',gamma=0.0069, C=1000

SVR_model.fit(X[51:],y[51:])

# regr = sk.svm.SVR(kernel='rbf')
# regr.fit(X, y)


# test output
precip_20 = []
for p in rain_20.iloc[:,1]:
    for i in range(21):
        precip_20.append(p)

dayOfYear = range(prices_20.shape[0])
test = np.column_stack((dayOfYear, precip_20))
out = SVR_model.predict(test)
print("Test Output:",out)
# print("Accuracy Score of the SVR Model is ", sk.metrics.accuracy_score(out, prices_20.iloc[:,1]))

plt.plot(dayOfYear,prices_20.iloc[:,1])
plt.plot(dayOfYear,out)

#plt.set_label("Ground Truth", "Predict")
plt.show()