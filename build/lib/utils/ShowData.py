# -*- coding: utf-8 -*-

import os
import cPickle as pickle
import time
import matplotlib.pyplot as plt
import numpy as np
from GlobalParam import *
from LoadData import unpickling


# bin_file list를 전달받아
# 각각의 bin_file을 그래프로 보여줌
def bins2graphs(file_list):

    for file in file_list:
        print 'vector2graph ' + file,

        x = []
        for line in unpickling(file)['ts']:
            x.append(line[0])
        y = unpickling(file)['value']

        plt.scatter(x, y, marker='x')

        file_name = file.rsplit('/', 1)[1]
        file_name = file_name.split('.')[0] + '.jpg'

        plt.title(file_name)
        plt.show()
        plt.close()
        print


# vector dictionary를 전달받아
# 각각의 vector를 그래프
def vectors2graphs(vectors):
    for i in xrange(len(vectors['file_name'])):
        name = vectors['file_name'][i].rsplit('/', 1)[1]
        print 'drawing graph of VECTORIZED ' + name,
        name = name.split('.')[0]
        name = name + '_vec_' + str(VEC_DIMENSION) + '.jpg'

        x = np.linspace(0, 1, len(vectors['vec_data'][i]))
        plt.scatter(x, vectors['vec_data'][i], marker='+')
        plt.title(name)
        plt.show()
        plt.close()
        print

