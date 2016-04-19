# -*- coding: utf-8 -*-

import time

from utils import Cluster
from utils import Data2Vec
from utils import LoadData
from utils import SaveData
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    abs_path = LoadData.get_directory()
    file_list = LoadData.load_file(abs_path)
    vector_dic = Data2Vec.bins2vectors2dic(file_list)
    clusters = Cluster.affinity_propagation(vector_dic)

    cluster_structure = Cluster.make_cluster_structure(vector_dic, clusters)

    print cluster_structure

    SaveData.cluster_structure2bin(abs_path, cluster_structure)

    # optional
    # for visualization
    # saver.clustered_graph(vector_dic['file_name'], clusters)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
