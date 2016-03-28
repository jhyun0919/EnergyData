# -*- coding: utf-8 -*-

import os
import sys
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt


def get_directory():
    try:
        dir_name = sys.argv[1]
        return dir_name
    except IndexError as err:
        print('IndexError: ' + str(err))
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


def draw_graph(file):
    y = unpickling(file)['value']

    i = np.linspace(0, 1, len(y))
    plt.scatter(i, y, marker='x')
    # plt.show()
    file_name = file.rsplit('/', 1)[-1]
    file_name = file_name.split('.')[0]
    file_name = file_name + '.jpg'
    print file_name
    plt.savefig(file_name)
    plt.close()

def unpickling(bin_file):
    data = pickle.load(open(bin_file))
    return data

if __name__ == "__main__":
    dir_name = get_directory()

    file_list = load_file(dir_name)

    for file in file_list:
        draw_graph(file)