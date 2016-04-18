# -*- coding: utf-8 -*-

from GlobalParam import *
from utils import LoadData
from utils import Data2Vec
from utils import SaveData
from utils import Classifier
import time
import os
import sys

if __name__ == "__main__":
    start_time = time.time()

    loader = LoadData()
    saver = SaveData(RESULT_DIRECTORY, VEC_DIMENSION, CLUSTER_STRUCTURE_NAME)
    d2v = Data2Vec(VEC_DIMENSION, INTERPOLATION_INTERVAL, SCALE_SIZE)
    clf = Classifier()

    CLUSTER_STRUCTURE_NAME = CLUSTER_STRUCTURE_NAME + '_' + str(VEC_DIMENSION) + '_vec.bin'

    file_path = os.path.join(os.getcwd(), RESULT_DIRECTORY, CLUSTER_STRUCTURE_NAME)
    cluster_structure = loader.unpickling(file_path)

    print cluster_structure

    clf = clf.train_clf(cluster_structure)

    print clf.predict(d2v.trim_data(sys.argv[1]))
    saver.bin2graph(sys.argv[1])

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'


