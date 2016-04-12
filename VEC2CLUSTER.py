# -*- coding: utf-8 -*-

from DATA2VEC import *
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt

AF_PREFERENCE = -10000
CLUSTER_STRUCTURE_NAME = 'cluster_structure.bin'

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
    # 출력 디렉토리로 이동
    # path_old = os.getcwd()
    path = os.path.join(os.getcwd(), RESULT_DIRECTORY, 'clustered_graph')
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    # 출력 디렉토리 내에서
    # 그래프를 그려 각각 cluster에 해당하는 폴더에 분류하여 저잫함
    for i in xrange(0, len(names)):
        path_temp = os.path.join(path, str(cluster[i]))
        if not os.path.exists(path_temp):
            os.makedirs(path_temp)
        os.chdir(path_temp)
        bin2graph(names[i])
        os.chdir(path)


def make_cluster_structure(vector_dic, cluster):
    cluster_structure = {}
    cluster_structure['file_name'] = vector_dic['file_name']
    cluster_structure['vector'] = vector_dic['data']
    cluster_structure['cluster_tag'] = cluster
    return cluster_structure


def save_cluster_structure(cluster_structure):
    path = os.path.join(os.getcwd(), RESULT_DIRECTORY)
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    bin_name = CLUSTER_STRUCTURE_NAME
    f = open(bin_name, 'wb')
    pickle.dump(cluster_structure, f, 1)
    f.close()


if __name__ == "__main__":
    start_time = time.time()

    dir_name = sys.argv[1]
    # dir_name = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_vec.bin'

    vector_dic = unpickling(dir_name)

    cluster = affinity_propagation(vector_dic)

    cluster_structure = make_cluster_structure(vector_dic, cluster)

    print cluster_structure

    save_cluster_structure(cluster_structure)

    # optional
    # for visualization
    clustered_graph(vector_dic['file_name'], cluster)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
