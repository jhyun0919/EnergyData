# -*- coding: utf-8 -*-

import Graph
import copy
import numpy as np
from GlobalParameter import *
import FileIO

from datetime import datetime


def interpolation():
    pass


def normalization(data_dictionary):
    """
    - normalization을 해주는 함수
    - Golbal_Parameter에서 정의된 Interpolation_Interval의 간격으로 normalization을 실행

    :param data_dictionary:
        original_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    :return:
        interpolated_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    """
    x = []
    y = []

    present_ts = data_dictionary['ts'][0][0].replace(second=0)
    minute_scanner = data_dictionary['ts'][0][0].minute / Interpolation_Interval
    present_ts = present_ts.replace(minute=minute_scanner * Interpolation_Interval)
    next_ts = present_ts + ts_delta

    value_collector = []

    for i in range(0, len(data_dictionary['ts'])):
        if data_dictionary['ts'][i][0] < next_ts:
            value_collector.append(data_dictionary['value'][i])

            # for final value
            if i == (len(data_dictionary['ts']) - 1):
                x.append(present_ts)
                calculated_value = sum(value_collector) / len(value_collector)
                y.append(calculated_value)

        else:
            x.append(present_ts)

            calculated_value = sum(value_collector) / len(value_collector)
            del value_collector[:]
            y.append(calculated_value)

            present_ts = next_ts
            next_ts = present_ts + ts_delta

            nan_number = ts_validity_checker(present_ts, data_dictionary['ts'][i][0])

            for i_nan in xrange(0, nan_number):
                x.append(present_ts)
                y.append(np.nan)

                present_ts = next_ts
                next_ts = present_ts + ts_delta

            value_collector.append(data_dictionary['value'][i])

    data_dictionary['ts'] = np.array(x)
    data_dictionary['value'] = np.array(y)

    return data_dictionary


def ts_validity_checker(present_ts, ts_index):
    validity_number = 0
    next_ts = present_ts + ts_delta
    while True:
        if next_ts >= ts_index:
            break
        elif next_ts < ts_index:
            validity_number += 1
            next_ts = next_ts + ts_delta

    return validity_number


def scaling(data_dictionary):
    """
    - scaling을 해주는 함수
    - Golbal_Parameter에서 정의된 Scale_Size에 따라 scaling 실행

   :param data_dictionary:
        original_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    :return:
        scaled_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    """
    data_list = data_dictionary['value']
    normalizer = n_th_abs_maximum(Noise_Filter, data_list)

    if normalizer == 0:
        pass
    else:
        data_dictionary['value'] = (data_list / normalizer) * Scale_Size

    return data_dictionary


def n_th_abs_maximum(n_th, data_list):
    """
    - Golbal_Parameter에서 정의된 Noise_Filter를 고려한 normalizer에 적당한 값 계산

    :param n_th:
        Noise_Filter
        - type: int
    :param data_list:
        data['value']
        - type: ndarray
    :return:
        normalizer_value
        - type: int
    """
    data_list_copy = copy.copy(data_list)
    data_list_copy.sort()

    return max(abs(data_list_copy[n_th]), data_list_copy[-n_th])


def data_preprocess(binary_file):
    """
    - binary file을 prepocessing 해주는 함수
    :param binary_file:
        binary file abs_path
    :return:
        preprocessed_dictionary = {"ts": ..., "value": ...}
    """
    data_dictionary = FileIO.Load.unpickling(binary_file)
    data_dictionary = scaling(normalization(data_dictionary))
    return data_dictionary


def preprocess4dependcy(binary_file_1, binary_file_2):
    """
    - 두 data 사이 dependency를 계산하기 위한 preprocessing 함수
    -

    :param binary_file_1:
        binary file abs_path
    :param binary_file_2:
        binary file abs_path
    :return:
    """
    data_dictionary_1 = data_preprocess(binary_file_1)
    data_dictionary_2 = data_preprocess(binary_file_2)

    early, late = start_time_compare(data_dictionary_1, data_dictionary_2)

    early, late = start_ts_synchronize(early, late)

    early, late, length = length_match(early, late)

    return early, late, length


def start_time_compare(data_dictionary_1, data_dictionary_2):
    """

    :param data_dictionary_1:
    :param data_dictionary_2:
    :return:
    """
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


def start_ts_synchronize(early, late):
    """

    :param early:
    :param late:
    :return:
    """
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
    """

    :param early:
    :param late:
    :return:
    """
    x, y = [], []
    if len(late['ts']) >= (len(early['ts'])):
        length = len(early['ts'])
        late['ts'] = late['ts'][0:length]

    else:
        length = len(late['ts'])
        early['ts'] = early['ts'][0:length]

    return early, late, length


if __name__ == '__main__':
    file_path = '/repository/VTT/VTT_GW1_HA10_VM_EP_KV_K.bin'

    Graph.Show.bin2graph(file_path)

    data_dictionary = FileIO.Load.unpickling(file_path)

    data_dictionary = normalization(data_dictionary)

    Graph.Show.dic2graph(data_dictionary)

    data_dictionary = scaling(data_dictionary)
    Graph.Show.dic2graph(data_dictionary)


    # def normalization(binary_file):
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
