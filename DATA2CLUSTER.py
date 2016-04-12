# -*- coding: utf-8 -*-

from GlobalParam import *
from utils import LoadData
from utils import Data2Vec
from utils import SaveData
from utils import Cluster
import time

if __name__ == "__main__":
    start_time = time.time()

    loader = LoadData()
    saver = SaveData(RESULT_DIRECTORY, VEC_DIMENSION, CLUSTER_STRUCTURE_NAME)
    d2v = Data2Vec(VEC_DIMENSION, INTERPOLATION_INTERVAL, SCALE_SIZE)
    clstr = Cluster(AF_PREFERENCE)

    dir_name = loader.get_directory()
    file_list = loader.load_file(dir_name)
    vector_dic = d2v.bins2vectors2dic(file_list)
    clusters = clstr.affinity_propagation(vector_dic)

    cluster_structure = clstr.make_cluster_structure(vector_dic, clusters)

    print cluster_structure

    saver.save_cluster_structure(cluster_structure)

    # optional
    # for visualization
    saver.clustered_graph(vector_dic['file_name'], clusters)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
