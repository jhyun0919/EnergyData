# -*- coding: utf-8 -*-

from sklearn import neighbors
import Graph
import copy
import numpy as np
from GlobalParameter import *
from Load import unpickling


def interpolation(data_dictionary):
    x = []
    y = []

    minute_scanner = data_dictionary['ts'][0][0].minute / Interpolation_Interval

    scanned_item = 0
    value_collector = 0

    for i in range(0, len(data_dictionary['ts'])):
        if data_dictionary['ts'][i][0].minute / Interpolation_Interval == minute_scanner:
            scanned_item += 1
            value_collector += data_dictionary['value'][i]
        else:
            if scanned_item == 0:
                # interpolation strategy
                # ============================
                y.append(y[-1])
                # ============================
            else:
                y.append(value_collector / scanned_item)
                value_collector = 0
                scanned_item = 0

            minute_scanner += 1
            if minute_scanner == 6:
                minute_scanner = 0

            i -= 1

            data_dictionary['ts'][i][0].replace(second=0)
            x.append(data_dictionary['ts'][i][0])

    if len(x) != len(y):
        print "interpolation error"
        exit()

    data_dictionary['ts'] = x
    data_dictionary['value'] = y

    return data_dictionary


def scaling(data_dictionary):
    data_list = data_dictionary['value']
    normalizer = n_th_abs_maximum(Noise_Filter, data_list)

    if normalizer == 0:
        pass
    else:
        data_dictionary['value'] = (np.array(data_list) / normalizer) * Scale_Size

    return data_dictionary


def n_th_abs_maximum(n_th, data_list):
    data_list_copy = copy.copy(data_list)
    data_list_copy.sort()

    return max(abs(data_list_copy[n_th]), data_list_copy[-n_th])


if __name__ == '__main__':
    file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_GW1_HA25_VM_KV_K.bin'

    Graph.Show.bin2graph(file_path)

    data_dictionary = unpickling(file_path)

    data_dictionary = interpolation(data_dictionary)

    Graph.Show.dic2graph(data_dictionary)

    data_dictionary = scaling(data_dictionary)
    Graph.Show.dic2graph(data_dictionary)


    # def interpolation(binary_file):
    #     data = unpickling(binary_file)
    #     X = data['ts']
    #     y = data['value']
    #
    #     time_stemp = date2sec(X, -1)
    #
    #     Y = np.zeros((1, time_stemp))[0].reshape((time_stemp, 1))
    #     for i in xrange (0, len(X)):
    #         temp = date2sec(X, i)
    #         Y[temp-1] = y[i]
    #     X = np.arange(0, time_stemp).reshape((time_stemp, 1))
    #     # T = np.arange(0, time_stemp).reshape((time_stemp, 1))
    #     T = np.linspace(0, time_stemp-1, time_stemp)[:, np.newaxis]
    #     print np.shape(T)
    #
    #     print len(X)
    #
    #
    #     knn = neighbors.KNeighborsRegressor(N_Neighbor, weights=Knn_Weights)
    #     y_ = knn.fit(X, Y).predict(T)
    #     #
    #     # plt.scatter(X, Y, c='k', label='data')
    #     # plt.plot(T, y_, c='g', label='prediction')
    #     # plt.axis('tight')
    #     # plt.legend()
    #     # plt.show()


    # def date2sec(date, i):
    #     delta = date[i] - date[0]
    #     days = delta[0].days
    #     return delta[0].seconds + (days * 24 * 60 * 60)
