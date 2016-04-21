# -*- coding: utf-8 -*-

import time
import numpy as np
import copy
from GlobalParam import *
from Load import unpickling
from Load import load_filelist


def bins2vectors2dic(path):
    vector_dic = {}
    data = []
    file_list = load_filelist(path)

    for file in file_list:
        try:
            print 'data2vector: ' + file.rsplit('/', 1)[1],
            start_time = time.time()
            data.append(trim_data(file))
        except:
            print '\t' + 'An error occurred',
        finally:
            end_time = time.time()
            print '\t' + 'run time: ' + str(end_time - start_time)

    vector_dic['vec_data'] = np.asarray(data)
    vector_dic['file_name'] = np.asarray(file_list)

    return vector_dic


# binary_file을 가공하여
# vector로 반환
def trim_data(bin_file):
    data = unpickling(bin_file)
    data = interpolation(data)
    data = normalization(data)
    vector_data = vectorization(data)

    return vector_data


# data를 입력받아
# 일정한 INTERPOLATION_INTERVAL로 가공한 뒤,
# list 형식으로 data 반환
def interpolation(data):
    y = []

    minute_check = data['ts'][0][0].minute / INTERPOLATION_INTERVAL
    item = 0
    value_collector = 0

    for i in range(0, len(data['ts'])):
        if data['ts'][i][2] / INTERPOLATION_INTERVAL == minute_check:
            item += 1
            value_collector += data['value'][i]
        else:
            minute_check += 1
            if minute_check == 6:
                minute_check = 0

            # 그 전 data value를 그대로 유지하는 strategy
            if item == 0:
                y.append(y[-1])
            else:
                y.append(value_collector / item)
                value_collector = 0
                item = 0
            i -= 1

    return y


# list 형식의 data를 입력받아
# SCALE_SIZE 범위 안으로 scaling 처리 한 뒤,
# list 형식으로 data 반환
def normalization(list):
    noise_filter = 10
    normalizer = n_th_maximum(noise_filter, list)

    if normalizer == 0:
        list_normalized = list
    else:
        list_normalized = np.array(list) / normalizer * SCALE_SIZE

    return list_normalized


# list를 입력받아
# 그 list의 n번째 최대값을
# 반환
def n_th_maximum(n_th, list):
    list_copy = copy.copy(list)
    list_copy.sort()
    return list_copy[-n_th]


# list 형식의 data를 입력받아
# VEC_DIMENSION의 차원으로 vector를 구성한 뒤,
# list 형식으로 data 반환
def vectorization(list):
    slicing_size = len(list) / VEC_DIMENSION
    vec = []
    vec_collector = 0

    for i in range(0, len(list)):
        vec_collector += list[i]
        if (i + 1) % slicing_size == 0:
            try:
                vec.append(int(vec_collector / slicing_size))
            except ValueError:
                # 0을 나누는 경우
                vec.append(0)
            except OverflowError:
                # 0으로 나누는 경우
                vec.append(-1000)
            finally:
                vec_collector = 0
    return vec
