import load_history
import datetime as dt
import trader

import numpy as np

from keras.models import Sequential
from keras.layers import Dense

MAS = [3,5,7, 15, 40, 100]
training_data = load_history.load_history(dt.datetime(2021,1,1), dt.datetime(2021, 4,1))
test_data = load_history.load_history(dt.datetime(2021,4,1), dt.datetime(2021,5,1))


def rel_dif(f,t):
    return (t-f)/t

def data2dataset(data):
    dset = []
    X = []
    Y = []
    for i in range(101,len(data)-10):
        X.append([])
        Y.append([])
        for j in MAS:
            X[-1].append(rel_dif(data[i-j][4],data[i][4]))
        y = 1 if data[i+1][4] > data[i][4] else 0
        Y[-1].append(y)
    return np.array(X),np.array(Y)

model = Sequential()
model.add(Dense(20, input_dim=len(MAS), activation='relu'))
model.add(Dense(15, activation='relu'))
model.add(Dense(9, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(1, activation='relu'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

X,Y = data2dataset(training_data)

model.fit(X,Y, epochs=50)


class Learning(trader.Trader):
    def __init__(self):
        super().__init__(self)
        self.counter = 0

    def strategy(self):
        MA = np.array([[
            self.ma[3],
            self.ma[5],
            self.ma[7],
            self.ma[15],
            self.ma[40],
            self.ma[100]
        ]])
        is_rising = model.predict(MA)[0][0]
        self.counter+=1
        print(self.counter, is_rising)
        if is_rising > 0.5:
            self.buy()
        else:
            self.sell()

final_value = Learning().run(test_data, verbose=True)
print(final_value)
