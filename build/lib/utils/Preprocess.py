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

            ###
            x_temp = data_dictionary['ts'][i][0].replace(second=0)
            x.append(x_temp)

    if len(x) != len(y):
        print "interpolation error"
        exit()

    data_dictionary['ts'] = np.array(x)
    data_dictionary['value'] = np.array(y)

    return data_dictionary


def scaling(data_dictionary):
    data_list = data_dictionary['value']
    normalizer = n_th_abs_maximum(Noise_Filter, data_list)

    if normalizer == 0:
        pass
    else:
        data_dictionary['value'] = (data_list / normalizer) * Scale_Size

    return data_dictionary


def n_th_abs_maximum(n_th, data_list):
    data_list_copy = copy.copy(data_list)
    data_list_copy.sort()

    return max(abs(data_list_copy[n_th]), data_list_copy[-n_th])


def preprocess4dependcy(binary_file_1, binary_file_2):
    data_dictionary_1 = unpickling(binary_file_1)
    data_dictionary_2 = unpickling(binary_file_2)

    data_dictionary_1 = scaling(interpolation(data_dictionary_1))
    data_dictionary_2 = scaling(interpolation(data_dictionary_2))

    early, late = time_compare(data_dictionary_1, data_dictionary_2)

    early, late = ts_synchronize(early, late)

    early, late, length = length_match(early, late)

    return early, late, length


def time_compare(data_dictionary_1, data_dictionary_2):
    if data_dictionary_1['ts'][0] > data_dictionary_2['ts'][0]:
        late = data_dictionary_1
        early = data_dictionary_2
    elif data_dictionary_1['ts'][0] < data_dictionary_2['ts'][0]:
        late = data_dictionary_2
        early = data_dictionary_1
    else:
        late = data_dictionary_1
        early = data_dictionary_2

    return early, late


def ts_synchronize(early, late):
    for i in xrange(0, len(early['ts'])):
        if late['ts'][0] == early['ts'][i]:
            ts_fix = i
            break

    x, y = [], []
    for i in xrange(ts_fix, len(early['ts'])):
        x.append(early['ts'][i])
        y.append((early['value'][i]))

    early['ts'] = np.array(x)
    early['value'] = np.array(y)

    return early, late


def length_match(early, late):
    x, y = [], []
    if len(late['ts']) >= (len(early['ts'])):
        length = len(early['ts'])
        for i in xrange(0, length):
            x.append(late['ts'][i])
            y.append((late['value'][i]))

        late['ts'] = np.array(x)
        late['value'] = np.array(y)

    else:
        length = len(late['ts'])
        for i in xrange(0, length):
            x.append(early['ts'][i])
            y.append((early['value'][i]))

        early['ts'] = np.array(x)
        early['value'] = np.array(y)

    return early, late, length


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
