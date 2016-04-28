# -*- coding: utf-8 -*-

import numpy as np
from sklearn import neighbors
from Graph import *
from GlobalParameter import *
from Load import unpickling


def interpolation(binary_file):
    data = unpickling(binary_file)
    X = data['ts']
    y = data['value']

    time_stemp = date2sec(X, -1)

    Y = np.zeros((1, time_stemp))[0].reshape((time_stemp, 1))
    for i in xrange (0, len(X)):
        temp = date2sec(X, i)
        Y[temp-1] = y[i]
    X = np.arange(0, time_stemp).reshape((time_stemp, 1))
    # T = np.arange(0, time_stemp).reshape((time_stemp, 1))
    T = np.linspace(0, time_stemp-1, time_stemp)[:, np.newaxis]
    print np.shape(T)

    print len(X)


    knn = neighbors.KNeighborsRegressor(N_Neighbor, weights=Knn_Weights)
    y_ = knn.fit(X, Y).predict(T)

    plt.scatter(X, Y, c='k', label='data')
    plt.plot(T, y_, c='g', label='prediction')
    plt.axis('tight')
    plt.legend()
    plt.show()


def date2sec(date, i):
    delta = date[i] - date[0]
    days = delta[0].days
    return delta[0].seconds + (days * 24 * 60 * 60)

if __name__ == '__main__':
    file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_GW1_HA25_VM_KV_K.bin'
    interpolation(file_path)
