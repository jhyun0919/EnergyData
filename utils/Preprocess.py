# -*- coding: utf-8 -*-

import numpy as np
from sklearn import neighbors
from Graph import *
from GlobalParameter import*
from Load import unpickling

def interpolation(binary_file):
    data = unpickling(binary_file)
    X = data['ts']
    T = np.linspace(0, 100, Interpolation_Interval)[:, np.newaxis]
    y = data['value']

    knn = neighbors.KNeighborsRegressor(N_Neighbor, weights=Knn_Weights)
    y_ = knn.fit(X, y).predict(T)

    plt.scatter(X, y, c='k', label='data')
    plt.plot(T, y_, c='g', label='prediction')
    plt.axis('tight')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_GW1_HA25_VM_KV_K.bin'
    interpolation(file_path)