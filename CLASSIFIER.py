# -*- coding: utf-8 -*-

import sys
import time

import os
from utils import Classifier
from utils import Data2Vec
from utils import LoadData
from utils import SaveData
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    CLUSTER_STRUCTURE_NAME = CLUSTER_STRUCTURE_NAME + '_' + str(VEC_DIMENSION) + '_vec.bin'

    file_path = os.path.join(os.getcwd(), RESULT_DIRECTORY, CLUSTER_STRUCTURE_NAME)
    cluster_structure = LoadData.unpickling(file_path)

    print cluster_structure

    clf = Classifier.train_clf(cluster_structure)

    print clf.predict(Data2Vec.trim_data(sys.argv[1]))
    SaveData.bin2graph(sys.argv[1])

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'


