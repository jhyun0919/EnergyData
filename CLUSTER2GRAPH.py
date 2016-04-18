# -*- coding: utf-8 -*-

from GlobalParam import *
from utils import LoadData
from utils import Data2Vec
from utils import SaveData
from utils import Cluster
import time
import sys

if __name__ == "__main__":
    start_time = time.time()

    loader = LoadData()
    saver = SaveData(RESULT_DIRECTORY, VEC_DIMENSION, CLUSTER_STRUCTURE_NAME)

    dir_name = sys.argv[1]
    cluster_stucture = loader.unpickling(dir_name)

    # optional
    # for visualization
    saver.clusters2graph(cluster_stucture)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'