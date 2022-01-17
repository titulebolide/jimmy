import datetime as dt
import trader
import os
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

cache = "cache_learning"
if not os.path.isdir(cache):
    os.mkdir(cache)
training_data = trader.load_history("VETUSDT-1m-data.csv",dt.datetime(2021,1,1), dt.datetime(2021,5,1))
test_data = trader.load_history("VETUSDT-1m-data.csv",dt.datetime(2021,5,1), dt.datetime(2021,6,1))

length = 300

def data2dataset(data):
    dset = []
    X = []
    Y = []
    for i in range(0,len(data)-length*2,length):
        X.append((data[i:i+length,4]-data[i,4])/data[i,4])
        Y.append((data[i+int(length*1.5),4]-data[i,4])/data[i,4]+0.5)
    return np.asarray(X).astype('float32'),np.asarray(Y).astype('float32')


model = Sequential()
model.add(Embedding(length, 128))
model.add(LSTM(128, dropout = 0.2, recurrent_dropout = 0.2))
model.add(Dense(1, activation = 'relu'))
model.compile(loss = 'binary_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())

model.compile(
    loss='mean_squared_error',
    optimizer="adam",
    metrics=["accuracy"]
)

X,Y = data2dataset(training_data)
print(X[0])
model.fit(X,Y, epochs=3)
model.save(os.path.join(cache, str(dt.datetime.now()).replace(" ", "T")))

print(model.predict(data2dataset(test_data)[0]))

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

#Learning(test_data).run(test_data, verbose=True)
