import datetime as dt
import trader
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

MAS = [1,2,3,4,5,6,7,8,9,10,15,40,100]
cache = "cache_learning"
if not os.path.isdir(cache):
    os.mkdir(cache)
training_data = trader.load_history("VETUSDT-1m-data.csv",dt.datetime(2021,1,1), dt.datetime(2021,5,1))
test_data = trader.load_history("VETUSDT-1m-data.csv",dt.datetime(2021,5,1), dt.datetime(2021,6,1))


def rel_dif(f,t):
    return (t-f)/t

def data2dataset(data):
    dset = []
    X_rising = []
    X_not_rising = []
    for i in range(101,len(data)-10):
        is_rising = rel_dif(data[i+1][4], data[i][4]) > 0
        X = X_rising
        if not is_rising:
            X = X_not_rising
        X.append([])
        for j in MAS:
            X[-1].append(rel_dif(data[i-j][4],data[i][4]))
    l = min(len(X_rising), len(X_not_rising))
    X_rising = X_rising[:l]
    X_not_rising = X_not_rising[:l]
    X = X_rising+X_not_rising
    Y = [1]*l+[0]*l
    return np.array(X),np.array(Y)

model = Sequential()
"""
model.add(Dense(300, input_dim=len(MAS), activation='relu'))
model.add(Dense(600, activation='relu'))
model.add(Dense(1200, activation='relu'))
model.add(Dense(600, activation='relu'))
model.add(Dense(250, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(24, activation='relu'))
"""
model.add(Dense(1, activation='relu'))


model.compile(
    loss='mean_squared_error',
    optimizer="adam",
    metrics=["accuracy"]
)

X,Y = data2dataset(training_data)

model.fit(X,Y, epochs=1)
model.save(os.path.join(cache, str(dt.datetime.now()).replace(" ", "T")))


class Learning(trader.Trader):
    def __init__(self, data):
        super().__init__(self)
        self.fees=0 #.075
        self.counter = 0
        self.X = []
        for i in range(101, len(data)):
            self.update_ma(data, i)
            self.X.append(list(self.ma.values()))
        print('start predicting')
        self.Y = model.predict(self.X)
        print('done')

    def strategy(self):
        is_rising = self.Y[self.data_index-101]
        #print(self.ma, self.X[self.data_index-101])
        self.counter+=1
        #print(self.counter, is_rising)
        if is_rising:
            self.buy()
        else:
            self.sell()

Learning(test_data).run(test_data, verbose=True)
