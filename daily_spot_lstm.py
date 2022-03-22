import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt


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

# test data 2020
prices_20 = pd.read_csv('./prices_2020.csv')
rain_20 = pd.read_csv('./rain_2020.csv')

# precipitation for the month that each day is in
precip = []
# day since begging of training data
dayOfYear = range(prices_train.shape[0])

for p in rain_train.iloc[:,1]:
    for i in range(21):
        precip.append(p)

# training inputs and outputs
X_train = np.column_stack((dayOfYear, precip)).astype(float)
Y_train = np.array(prices_train.iloc[:,1]).astype(float)
Y_train_norm = np.array(prices_train.iloc[:,1]).astype(float)
Y_train_norm[0] = 0

# normalize price data to percent changes
for i in range(1,Y_train.size):
    Y_train_norm[i] = (Y_train[i]-Y_train[i-1])/Y_train[i-1]

#print(X_train[:][0:10])
#print(Y_train_norm[0:5])

# drop first value as due to normalization
X_train_tensors = Variable(torch.Tensor(X_train[:][1:]))
y_train_tensors = Variable(torch.Tensor(Y_train_norm[1:]))

X_train_tensors = torch.reshape(X_train_tensors,   (X_train_tensors.shape[0], 1, X_train_tensors.shape[1]))
y_train_tensors = torch.reshape(y_train_tensors,   (X_train_tensors.shape[0], 1))


print("Training Shape", X_train_tensors.shape, y_train_tensors.shape)

torch.manual_seed(1)

class LSTMSpot1(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length):
        super(LSTMSpot1, self).__init__()
        self.num_classes = num_classes #number of classes
        self.num_layers = num_layers #number of layers
        self.input_size = input_size #input size
        self.hidden_size = hidden_size #hidden state
        self.seq_length = seq_length #sequence length

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True) #lstm

        self.fc_1 =  nn.Linear(hidden_size, 128) #fully connected 1
        self.fc = nn.Linear(128, num_classes) #fully connected last layer

        self.relu = nn.ReLU()

    def forward(self,x):
        h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #hidden state
        c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #internal state
        # Propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input, hidden, and internal state
        hn = hn.view(-1, self.hidden_size) #reshaping the data for Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out) #first Dense
        out = self.relu(out) #relu
        out = self.fc(out) #Final Output
        return out

class LSTMSpot2(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length, drop_prob=0.2):
        super(LSTMSpot1, self).__init__()
        self.num_classes = num_classes #number of classes
        self.num_layers = num_layers #number of layers
        self.input_size = input_size #input size
        self.hidden_size = hidden_size #hidden state LSTM size
        self.seq_length = seq_length #sequence length

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=False,
                            dropout=drop_prob) #lstm

        self.fc_1 =  nn.Linear(hidden_size, 128) #fully connected 1
        self.fc = nn.Linear(128, num_classes) #fully connected last layer

        self.dropout = nn.Dropout(drop_prob)

        self.relu = nn.ReLU()


    def forward(self,x):
        h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #hidden state
        c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #internal state
        # Propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input, hidden, and internal state
        hn = hn.view(-1, self.hidden_size) #reshaping the data for Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out) #first Dense
        out = self.relu(out) #relu
        out = self.drop_out(self.fc(out)) #Final Output
        return out


num_epochs = 1000 # epochs
learning_rate = 0.001 #0.001 lr

input_size = 2 #number of features
hidden_size = 64 #number of features in hidden state
num_layers = 1 #number of stacked lstm layers

num_classes = 1 #number of output classes

lstm1 = LSTMSpot1(num_classes, input_size, hidden_size, num_layers, X_train_tensors.shape[1]) #our lstm class

criterion = torch.nn.MSELoss()    # mean-squared error for regression
optimizer = torch.optim.Adam(lstm1.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
  outputs = lstm1.forward(X_train_tensors) #forward pass
  optimizer.zero_grad() #caluclate the gradient, manually setting to 0

  # obtain the loss function
  loss = criterion(outputs, y_train_tensors)

  loss.backward() #calculates the loss of the loss function

  optimizer.step() #improve from loss, i.e backprop
  if epoch % 100 == 0:
    print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))

# Test on test data

testDayOfYear = range(dayOfYear[len(dayOfYear)-1], dayOfYear[len(dayOfYear)-1] + prices_20.shape[0])
test_precip = []

for p in rain_20.iloc[:,1]:
    for i in range(21):
        test_precip.append(p)

X_test = np.column_stack((testDayOfYear, test_precip)).astype(float)
Y_test = np.array(prices_20.iloc[:,1]).astype(float)

X_test_tensors = Variable(torch.Tensor(X_test))
Y_test_tensor = Variable(torch.Tensor(Y_test))



X_test_tensors = torch.reshape(X_test_tensors,   (X_test_tensors.shape[0], 1, X_test_tensors.shape[1]))
print("Testing Shape", X_test_tensors.shape, Y_test.shape)

test_predict_norm = lstm1(X_test_tensors)#forward pass
data_predict_norm = test_predict_norm.data.numpy() #numpy conversion
dataY_plot = Y_test_tensor.data.numpy()

start_price = Y_train[-1]
print("start: ", start_price)
print(data_predict_norm.shape)

data_predict = test_predict_norm.data.numpy() #numpy conversion
data_predict[0] = start_price

for i in range(1,data_predict_norm.size):
    data_predict[i] = data_predict_norm[i]*data_predict[i-1] + data_predict[i-1]




plt.figure(figsize=(10,6)) #plotting
#plt.axvline(x=200, c='r', linestyle='--') #size of the training set

plt.plot(dataY_plot, label='Actuall Data') #actual plot
plt.plot(data_predict, label='Predicted Data') #predicted plot
plt.title('Time-Series Prediction')
plt.legend()
plt.show()

# Test on train data

train_predict_norm = lstm1(X_train_tensors)#forward pass
train_data_predict_norm = train_predict_norm.data.numpy() #numpy conversion
train_dataY_plot = Y_test_tensor.data.numpy()

start_price = Y_train[0]
print("start: ", start_price)
print(train_data_predict_norm.shape)

train_data_predict = train_predict_norm.data.numpy() #numpy conversion
train_data_predict[0] = start_price

for i in range(1,train_data_predict.size):
    train_data_predict[i] = train_data_predict_norm[i]*train_data_predict[i-1] + train_data_predict[i-1]


plt.figure(figsize=(10,6)) #plotting
#plt.axvline(x=200, c='r', linestyle='--') #size of the training set

plt.plot(train_dataY_plot, label='Actuall Data') #actual plot
plt.plot(train_data_predict, label='Predicted Data') #predicted plot
plt.title('Time-Series Prediction')
plt.legend()
plt.show()


