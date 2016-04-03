# -*- coding: utf-8 -*-

from DATA2VEC import *
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt

AF_PREFERENCE = -5000


def bin2graph(file):
    print 'vector 2 graph ' + file,
    start_time = time.time()

    x = []
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


def affinity_propagation(vector_dic):
    vectors = vector_dic['data']
    return AffinityPropagation(preference=AF_PREFERENCE).fit_predict(vectors)


def clustered_graph(names, cluster):
    path = os.path.join(os.getcwd(), get_directory(), 'clustered_graph')
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


if __name__ == "__main__":
    start_time = time.time()

    dir_name = sys.argv[1]
    # dir_name = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_vec.bin'

    vector_dic = unpickling(dir_name)

    cluster = affinity_propagation(vector_dic)

    print cluster

    clustered_graph(vector_dic['file_name'], cluster)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
