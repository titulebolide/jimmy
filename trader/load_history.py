import csv
import datetime as dt
import numpy as np
import os

def load_history(filename, start=dt.datetime(2000,1,1), end=dt.datetime(2100,1,1)):
    cache_folder = 'cache_history'
    cache_file = os.path.join(cache_folder,filename+'.npy')
    data = []
    if not os.path.isdir(cache_folder):
        os.mkdir(cache_folder)
    if not os.path.isfile(cache_file):
        with open(filename) as f:
            for line in csv.reader(f):
                if line[0] == 'timestamp':
                    continue
                line[0] = dt.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")
                timestamp = line[0]
                for i in range(1, len(line)):
                    line[i] = float(line[i])
                data.append(line)
        np.save(cache_file, data, allow_pickle=True)
    else:
        data = np.load(cache_file, allow_pickle=True)

    data_dates = []
    for line in data:
        if start < line[0] < end:
            data_dates.append(line)

    data_dates = np.array(data_dates)

    return data_dates
