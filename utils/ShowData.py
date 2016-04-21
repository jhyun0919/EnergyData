# -*- coding: utf-8 -*-

import os
import cPickle as pickle
import time
import matplotlib.pyplot as plt
import numpy as np
from GlobalParam import *
from Load import unpickling


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


def clusters2graph(path, cluster_structure):
    old_path = os.getcwd()

    # names = cluster_structure['file_name']
    # clusters = cluster_structure['cluster_tag']

    # 출력 디렉토리로 이동
    # path_old = os.getcwd()
    path = os.path.join(path, RESULT_DIRECTORY, 'clustered_graph', str(VEC_DIMENSION))
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    # 출력 디렉토리 내에서
    # 그래프를 그려 각각 clusters에 해당하는 폴더에 분류하여 저잫함
    for i in xrange(0, len(cluster_structure['file_name'])):
        path_temp = os.path.join(path, str(cluster_structure['cluster_tag'][i]))
        if not os.path.exists(path_temp):
            os.makedirs(path_temp)
        os.chdir(path_temp)
        bin2graph(cluster_structure['file_name'][i])
        os.chdir(path)

    os.chdir(old_path)
