# -*- coding: utf-8 -*-

import os
import sys
import cPickle as pickle
import numpy as np
import time
import matplotlib.pyplot as plt
import types


def get_directory():
    try:
        dir_name = sys.argv[1]
        return dir_name
    except IndexError as err:
        print('IndexError: ' + str(err))
        print('Put a directory path as an input argument')
        exit()

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
        print('OSError' + str(err))


    return file_list


def bin2graph(file):
    print 'working on ' + file,
    start_time = time.time()

    x= []
    for line in unpickling(file)['ts']:
        x.append(line[0])
    y = unpickling(file)['value']


    plt.scatter(x, y, marker='x')

    file_path, file_name = file.rsplit('/', 1)
    file_path = os.path.join(file_path, 'graph')

    if not os.path.exists(file_path):
        os.mkdir(file_path)
    os.chdir(file_path)
    file_name = file_name.split('.')[0]
    file_name = file_name + '.jpg'

    plt.savefig(file_name)
    plt.close()

    end_time = time.time()
    print '\t\t' + 'run time: ' + str(end_time - start_time)

def unpickling(bin_file):
    data = pickle.load(open(bin_file))
    return data

if __name__ == "__main__":
    ST = time.time()

    dir_name = get_directory()

    file_list = load_file(dir_name)

    for file in file_list:
        bin2graph(file)



    ET = time.time()

    print '*** TOATL TIME: ' + str(ET - ST) + ' ***'