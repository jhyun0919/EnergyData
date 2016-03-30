# -*- coding: utf-8 -*-

import sys
import os
import time
import matplotlib.pyplot as plt
import cPickle as pickle
from sklearn.cluster import KMeans


def unpickling(bin_file):
    data = pickle.load(open(bin_file))
    return data


def bin2graph(file):
    print 'working on ' + file,
    start_time = time.time()

    x= []
    for line in unpickling(file)['ts']:
        x.append(line[0])
    y = unpickling(file)['value']

    plt.scatter(x, y, marker='x')

    file_name = file.rsplit('/', 1)[-1]

    file_name = file_name.split('.')[0]
    file_name = file_name + '.jpg'

    plt.savefig(file_name)
    plt.close()

    end_time = time.time()
    print '\t\t' + 'run time: ' + str(end_time - start_time)


def kmeans(vectors_dic):
    vectors = vectors_dic['data']
    return KMeans (n_clusters=5, verbose=True).fit_predict(vectors)



def clustered_graph(names, cluster):
    path = os.path.join(os.getcwd(), 'clustered_graph')
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    for i in xrange(0, len(names)):
        path_temp = os.path.join(path, str(cluster[i]))
        if not os.path.exists(path_temp):
            os.makedirs(path_temp)
        os.chdir(path_temp)
        bin2graph(names[i])
        os.chdir(path)




# directory = sys.argv[1]
file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_vec.bin'

vec_data = pickle.load(open(file_path))

names = vec_data['file_name']
vectors = vec_data['data']

cluster = KMeans (n_clusters=5, verbose=True).fit_predict(vectors)

for name in names:
    print name

print cluster

clustered_graph(names, cluster)

