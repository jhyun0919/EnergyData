# -*- coding: utf-8 -*-

import os
import sys
import cPickle as pickle
import numpy as np
import copy
import time
import types
import matplotlib.pyplot as plt

VEC_DIMENSION = 40
INTERPOLATION_INTERVAL = 10 # -> minute
SCALE_SIZE = 100


# 인자로 전달된 디렉토리를 반환
def get_directory():
    try:
        dir_name = sys.argv[1]
        return dir_name
    except IndexError as err:
        print('IndexError: ' + str(err))
        exit()


# 파일리스트를 만들어 반환
def load_file(dir_name):
    file_list = []

    try:
        file_names = os.listdir(dir_name)
        abs_dir = os.path.dirname(os.path.abspath(__file__))

        for file_name in file_names:
            full_filename = os.path.join(dir_name, file_name)
            ext = os.path.splitext(full_filename)[-1]
            if ext == '.bin':
                file = os.path.join(abs_dir, dir_name, file_name)
                file_list.append(file)
    except OSError as err:
        print 'OSError' + str(err)


    return file_list


# binary data를 가공하여 반환
def trim_data(bin_file):
    data = pickle.load(open(bin_file))
    data = interpolation(data)
    data = normalization(data)
    vector_data = vectorization(data)

    return vector_data

# 일정한 간격으로 interpolation 된 data를 list형식으로 반환
def interpolation(data):
    # x = []
    y = []

    minute_check = data['ts'][0][0].minute / INTERPOLATION_INTERVAL
    item = 0
    value_collector = 0

    for i in range(0, len(data['ts'])):
        if data['ts'][i][2] / INTERPOLATION_INTERVAL == minute_check:
            item += 1
            value_collector += data['value'][i]
        else:
            # ts 간격 일정하게 조정
            # x.append(data['ts'][i - 1][0].replace(minute=10 * minute_check, second=0))

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


# 일정한 크기로 scale을 normalization된 data를 반환
def normalization(list):
    noise_filter = 10

    normalizer = n_th_maximum(noise_filter, list)
    print
    print normalizer

    if normalizer == 0:
        list_normalized = list
    else:
        list_normalized = np.array(list) / normalizer * SCALE_SIZE

    return list_normalized


def n_th_maximum(n_th, list):
    list_copy = copy.copy(list)
    list_copy.sort()
    return list_copy[-n_th]


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
                vec.append(0)
            except OverflowError:
                vec.append(-100)
            finally:
                vec_collector = 0
    return vec


def draw_vec_graph(name, vec_value):
    path, name = name.rsplit('/', 1)

    path = path + '/graph'

    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)

    name = name.split('.')[0]
    name = name + '_vec_'+str(VEC_DIMENSION) +'.jpg'

    x = np.linspace(0, 1, len(vec_value))
    plt.scatter(x, vec_value, marker='+')
    plt.savefig(name)
    plt.close()


def save_as_txt(vec_dic):
    f = open("vector.txt", 'w')

    for vec in vec_dic:
        f.write(vec+'\n')
        f.write(str(vec_dic[vec])+'\n')

    f.close()

def save_as_bin(vec_dic):
    f = open("vector.bin", 'wb')
    pickle.dump(vec_dic, f, 1)
    f.close()


# main function
if __name__ == "__main__":
    ST = time.time()

    dir_name = get_directory()

    file_list = load_file(dir_name)

    vector_dic = {}
    # {'file_path' : vector}

    for file in file_list:
        try:
            print 'working on ' + file,
            start_time = time.time()
            vector_dic[file] = trim_data(file)
        except:
            print 'An error occurred'
            # exit()
        finally:
            end_time = time.time()
            print '\t\t' + 'run time: ' + str(end_time - start_time)

    # for i in range (0, len(vector_dic)):
    #     print vector_dic.keys()[i]
    #     print vector_dic[vector_dic.keys()[i]]
    #     draw_vec_graph(vector_dic.keys()[i], vector_dic[vector_dic.keys()[i]])


    # 매번 변환 할 수 없으니 bin file로 저장하자

    save_as_bin(vector_dic)



    ET = time.time()

    print
    print '*** TOATL TIME: ' + str(ET - ST) + ' ***'

