# -*- coding: utf-8 -*-

import os
import sys
import cPickle as pickle
import numpy as np
from sklearn.cluster import KMeans
import copy
import matplotlib.pyplot as plt


def file_directory():
    try:
        dirname = sys.argv[1]
        return dirname
    except IndexError as err:
        print('IndexError: ' + str(err))
        exit()


def load_file(dirname):
    file_list = []
    filenames = os.listdir(dirname)
    abs_dir = os.path.dirname(os.path.abspath(__file__))

    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.bin':
            file = os.path.join(abs_dir, dirname, filename)
            file_list.append(trim_data(file))

    return file_list


def trim_data(binfile):
    data = pickle.load(open(binfile))
    vector_data = vectorization(normalization(interpolation(data['ts'], data['value'])))
    return vector_data


def interpolation(ts, value):
    x, y = [], []

    minute_check = ts[0][0].minute / 10
    item = 0

    value_temp = 0

    for i in range(0, len(ts)):
        if ts[i][2] / 10 == minute_check:
            item += 1
            value_temp += value[i]
        else:
            x.append(ts[i - 1][0].replace(minute=10 * minute_check, second=0))

            minute_check += 1
            if minute_check == 6:
                minute_check = 0

            if item == 0:
                y.append(y[-1])
            else:
                y.append(value_temp / item)
                value_temp = 0
                item = 0

            i = i - 1

    return y


def normalization(list):
    filter = 100
    while True:
        normalizer = n_th_maximun(filter, list)
        if normalizer != 0:
            break
        else:
            filter = filter - 10
        if filter == 0:
            normalizer = 1

    list_normalized = np.array(list) / normalizer * 100
    return list_normalized


def n_th_maximun(n_th, list):
    list_copy = copy.copy(list)
    list_copy.sort()
    return list[-n_th]


def vectorization(list):
    dim = 20
    slicing_size = len(list) / dim
    vec = []
    vec_collector = 0

    for i in range(0, len(list)):
        vec_collector += list[i]
        if (i + 1) % slicing_size == 0:
            try:
                vec.append(int(vec_collector / slicing_size))
            except ValueError as verr:
                vec.append(0)
            except OverflowError as oerr:
                vec.append(-100)
            finally:
                vec_collector = 0
    return vec


def draw_graph(y):
    i = np.linspace(0, 1, len(y))
    plt.scatter(i, y, marker='x')
    plt.show()


if __name__ == "__main__":
    vector_list = load_file(file_directory())
    for vec in vector_list:
        print vec

