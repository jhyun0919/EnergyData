# -*- coding: utf-8 -*-

from Load import unpickling
from GlobalParameter import *
from Preprocess import interpolation
from Preprocess import scaling
import Graph

import matplotlib.pyplot as plt
import numpy as np


def similarity_score(data_dictionary_1, data_dictionary_2):
    similarity = []

    if data_dictionary_1['ts'][0][0] > data_dictionary_2['ts'][0][0]:
        late = data_dictionary_1
        early = data_dictionary_2
    elif data_dictionary_1['ts'][0][0] < data_dictionary_2['ts'][0][0]:
        late = data_dictionary_2
        early = data_dictionary_1
    else:
        late = data_dictionary_1
        early = data_dictionary_2

    late = scaling(interpolation(late))
    early = scaling(interpolation(early))

    print early

    for i in xrange(0, len(early['ts'])):
        if late['ts'][0][0] == early['ts'][i][0]:
            ts_fix = i
            break

    print ts_fix

    if len(late['ts']) >= (len(early['ts']) - ts_fix):
        ts_total = len(early['ts']) - ts_fix
    else:
        ts_total = len(late['ts'])

    Graph.Show.dic2graph(late)
    Graph.Show.dic2graph(early)

    for i in xrange(0, ts_total):
        early_data = early['value'][i + ts_fix] / Level
        late_data = late['value'][i] / Level

        if early_data == late_data:
            similarity.append(1)
        else:
            similarity.append(0)

    print ts_total
    x = np.linspace(0, ts_total, ts_total)
    print len(x)
    print len(similarity)

    plt.scatter(x, similarity)
    plt.show()
    plt.close()

    counter = 0
    for i in similarity:
        if i == 1:
            counter += 1
    similarity_rate = float(counter) / ts_total

    return similarity_rate


def dependency_model():
    pass


def close_dependency():
    pass


def far_dependency():
    pass


def time_sync(data_dictionary_1, data_dictionary_2):
    syncronized_early = {}
    syncronized_late = {}

    if data_dictionary_1['ts'][0][0] > data_dictionary_2['ts'][0][0]:
        late = data_dictionary_1
        early = data_dictionary_2
    elif data_dictionary_1['ts'][0][0] < data_dictionary_2['ts'][0][0]:
        late = data_dictionary_2
        early = data_dictionary_1
    else:
        late = data_dictionary_1
        early = data_dictionary_2

    late = scaling(interpolation(late))
    early = scaling(interpolation(early))

    return syncronized_early, syncronized_late


if __name__ == '__main__':
    file_path_1 = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_GW1_HA10_VM_EP_KV_K.bin'
    file_path_2 = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_GW1_HA10_VM_KV_K.bin'

    data_dictionary_1 = unpickling(file_path_1)
    data_dictionary_2 = unpickling(file_path_2)

    print data_dictionary_1

    score = similarity_score(data_dictionary_1, data_dictionary_2)

    print score
