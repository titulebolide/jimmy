import csv
import datetime as dt
import numpy as np
import os

def load_history(start=dt.datetime(2000,1,1), end=dt.datetime(2100,1,1)):
    data = []
    if not os.path.isfile('cache.npy'):
        with open('DOGEUSDT-1m-data.csv') as f:
            for line in csv.reader(f):
                if line[0] == 'timestamp':
                    continue
                line[0] = dt.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")
                timestamp = line[0]
                for i in range(1, len(line)):
                    line[i] = float(line[i])
                data.append(line)
        np.save('cache.npy', data, allow_pickle=True)
    else:
        data = np.load('cache.npy', allow_pickle=True)


    data_dates = []
    for line in data:
        if start < line[0] < end:
            data_dates.append(line)

    return data_dates
