# -*- coding: utf-8 -*-

import sys
import time

from utils import Load
from utils import Save
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    loader = Load()
    saver = Save(RESULT_DIRECTORY, VEC_DIMENSION, CLUSTER_STRUCTURE_NAME)

    dir_name = sys.argv[1]
    cluster_stucture = loader.unpickling(dir_name)

    # optional
    # for visualization
    saver.clusters2graph(cluster_stucture)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'