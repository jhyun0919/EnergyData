# -*- coding: utf-8 -*-

import sys
import time

from utils import Load
from utils import ModelDependency
from utils import Save
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    loader = Load()
    saver = Save(RESULT_DIRECTORY, VEC_DIMENSION, CLUSTER_STRUCTURE_NAME)
    mdl_dpncy = ModelDependency()

    dir_name = sys.argv[1]
    cluster_stucture = loader.unpickling(dir_name)

    model_dependency = mdl_dpncy.cluster2modeldependency(cluster_stucture)

    print model_dependency

    saver.dependency2bin(model_dependency)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
