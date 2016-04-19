# -*- coding: utf-8 -*-

import sys
import time

from utils import Cluster
from utils import Data2Vec
from utils import LoadData
from utils import SaveData
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    loader = LoadData()
    saver = SaveData(RESULT_DIRECTORY, VEC_DIMENSION, CLUSTER_STRUCTURE_NAME)
    d2v = Data2Vec(VEC_DIMENSION, INTERPOLATION_INTERVAL, SCALE_SIZE)
    clstr = Cluster(AF_PREFERENCE)

    dir_name = sys.argv[1]
    # dir_name = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT_vec.bin'

    vector_dic = loader.unpickling(dir_name)

    cluster = clstr.affinity_propagation(vector_dic)

    cluster_structure = clstr.make_cluster_structure(vector_dic, cluster)

    print cluster_structure

    saver.cluster_structure2bin(cluster_structure)


    # optional
    # for visualization
    # saver.clustered_graph(vector_dic['file_name'], cluster)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
