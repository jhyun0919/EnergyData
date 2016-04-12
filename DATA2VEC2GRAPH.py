# -*- coding: utf-8 -*-

from GlobalParam import *
from utils import LoadData
from utils import SaveData
from utils import Data2Vec
import time

# main function
if __name__ == "__main__":
    start_time = time.time()

    loader = LoadData()
    saver = SaveData(RESULT_DIRECTORY, VEC_DIMENSION)
    d2v = Data2Vec(VEC_DIMENSION, INTERPOLATION_INTERVAL, SCALE_SIZE)

    dir_name = loader.get_directory()

    file_list = loader.load_file(dir_name)

    vector_dic = d2v.bins2vectors2dic(file_list)

    saver.vectors2graphs(vector_dic)

    end_time = time.time()

    print
    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
