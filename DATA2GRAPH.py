# -*- coding: utf-8 -*-

# import os
# import sys
# import cPickle as pickle
# import time
# import matplotlib.pyplot as plt

from DATA2VEC import *


def bin2graph(file_list):
    for file in file_list:
        print 'working on ' + file,
        start_time = time.time()

        x = []
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


if __name__ == "__main__":
    start_time = time.time()

    dir_name = get_directory()

    file_list = load_file(dir_name)

    bin2graph(file_list)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
