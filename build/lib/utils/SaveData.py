# -*- coding: utf-8 -*-

import os
import cPickle as pickle
import time
import matplotlib.pyplot as plt
import numpy as np
from GlobalParam import *
from LoadData import unpickling


# def __init__(self, RESULT_DIRECTORY, VEC_DIMENSION=None, CLUSTER_STRUCTURE_NAME=None):
#     self.RESULT_DIRECTORY = RESULT_DIRECTORY
#
#     if VEC_DIMENSION is not None:
#         self.VEC_DIMENSION = VEC_DIMENSION
#
#     if CLUSTER_STRUCTURE_NAME is not None:
#         self.CLUSTER_STRUCTURE_NAME = CLUSTER_STRUCTURE_NAME



# vector_dictionary를
# binary_file로 바꾸어
# RESULT_DICETORY에 저장
def dictionary2bin(path, vec_dic):
    old_path = os.getcwd()

    path = os.path.join(path, RESULT_DIRECTORY)
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    bin_name = path + '/vectorized_data_dim_' + str(VEC_DIMENSION) + '.bin'

    f = open(bin_name, 'wb')
    pickle.dump(vec_dic, f, 1)
    f.close()

    os.chdir(old_path)


# vector_dictionary를
# text_file로 바꾸어
# RESULT_DICETORY에 저장
def dictionary2txt(path, vec_dic):
    old_path = os.getcwd()

    path = os.path.join(path, RESULT_DIRECTORY)
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    txt_name = path + '_' + '/vectorized_data_dim_' + str(VEC_DIMENSION) + '.txt'

    f = open(txt_name, 'w')
    for line in vec_dic:
        f.write(line + '\n')
        for i in xrange(len(vec_dic[line])):
            f.write(str(vec_dic[line][i]) + '\n')
    f.close()

    os.chdir(old_path)


# bin_file list를 전달받아
# 각각의 bin_file을 그래프로 그려
# RESULT_DIRECTORY에 저장함
def bins2graphs(path, file_list):
    old_path = os.getcwd()

    path = os.path.join(path, RESULT_DIRECTORY, 'graph')
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    for file in file_list:
        print 'vector2graph ' + file,
        start_time = time.time()

        x = []
        for line in unpickling(file)['ts']:
            x.append(line[0])
        y = unpickling(file)['value']

        plt.scatter(x, y, marker='x')

        file_name = file.rsplit('/', 1)[1]

        file_name = file_name.split('.')[0] + '.jpg'

        plt.title(file_name)
        plt.savefig(file_name)
        plt.close()

        end_time = time.time()
        print '\t\t' + 'run time: ' + str(end_time - start_time)

    os.chdir(old_path)


# bin_file을 전달받아
# 그래프로 그려
# 현재의 경로에 저장힘
def bin2graph(file):
    start_time = time.time()
    print 'vector 2 graph ' + file,

    x = []
    for line in unpickling(file)['ts']:
        x.append(line[0])
    y = unpickling(file)['value']

    plt.scatter(x, y, marker='x')

    file_name = file.rsplit('/', 1)[-1]

    file_name = file_name.split('.')[0] + '.jpg'

    plt.savefig(file_name)
    plt.close()

    end_time = time.time()

    print '\t\t' + 'run time: ' + str(end_time - start_time)


# vector dictionary를 전달받아
# 각각의 vector를 그래프로 그려
# RESULT_DIRECTORY에 저장함
def vectors2graphs(path, vectors):
    old_path = os.getcwd()

    path = os.path.join(path, RESULT_DIRECTORY, 'graph', 'vectorize', str(VEC_DIMENSION))
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    for i in xrange(len(vectors['file_name'])):
        start_time = time.time()

        name = vectors['file_name'][i].rsplit('/', 1)[1]

        print 'drawing graph of VECTORIZED ' + name,

        name = name.split('.')[0]
        name = name + '_vec_' + str(VEC_DIMENSION) + '.jpg'

        x = np.linspace(0, 1, len(vectors['vec_data'][i]))
        plt.scatter(x, vectors['vec_data'][i], marker='+')
        plt.title(name)
        plt.savefig(name)
        plt.close()

        end_time = time.time()

        print '\t\t' + 'run time: ' + str(end_time - start_time)

    os.chdir(old_path)


# bin_file의 이름 list인 names와
# clusters를 전달받아
# 각각의 bin_file을 그래프로 그려
# cluster에 따라 분류하여
# RESULT_DIRECTORY에 저장함
def clusters2graph(cluster_structure):
    old_path = os.getcwd()

    # names = cluster_structure['file_name']
    # clusters = cluster_structure['cluster_tag']

    # 출력 디렉토리로 이동
    # path_old = os.getcwd()
    path = os.path.join(os.getcwd(), RESULT_DIRECTORY, 'clustered_graph', str(VEC_DIMENSION))
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


# cluster_structure를 입력받아
# binary file로 변환 후
# RESULT_DIRECTORY에 저장함
def cluster_structure2bin(path, cluster_structure):
    old_path = os.getcwd()

    path = os.path.join(path, RESULT_DIRECTORY)
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    path = os.path.join(path, CLUSTER_STRUCTURE_NAME)
    bin_name = path + '_dim_' + str(VEC_DIMENSION) + '.bin'
    f = open(bin_name, 'wb')
    pickle.dump(cluster_structure, f, 1)
    f.close()

    os.chdir(old_path)


# dependency를
# binary_file로 바꾸어
# RESULT_DICETORY에 저장
def dependency2bin(dependency_dic):
    old_path = os.getcwd()

    path = os.path.join(os.getcwd(), RESULT_DIRECTORY)
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    bin_name = 'dependency.bin'

    f = open(bin_name, 'wb')
    pickle.dump(dependency_dic, f, 1)
    f.close()

    os.chdir(old_path)

# dependency를
# text_file로 바꾸어
# RESULT_DICETORY에 저장
def dependency2txt(dependency_dic):
    old_path = os.getcwd()

    path = os.path.join(os.getcwd(), RESULT_DIRECTORY)
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    txt_name = 'dependency.txt'

    f = open(txt_name, 'w')
    for line in dependency_dic:
        f.write(line + '\n')
        for i in xrange(len(dependency_dic[line])):
            f.write(str(dependency_dic[line][i]) + '\n')
    f.close()

    os.chdir(old_path)
