# -*- coding: utf-8 -*-

# This module gets a directory path as an input argument and
# makes a binary file of vectorized data.

# >>> python DATA2VEC.py <directory>

from GlobalParam import *
from utils import LoadData
from utils import Data2Vec
from utils import SaveData
import time

if __name__ == "__main__":
    start_time = time.time()

    loader = LoadData()
    saver = SaveData(RESULT_DIRECTORY, VEC_DIMENSION)
    d2v = Data2Vec(VEC_DIMENSION, INTERPOLATION_INTERVAL, SCALE_SIZE)

    # get directory path
    dir_name = loader.get_directory()

    # make a list of files from the path
    file_list = loader.load_file(dir_name)

    # convert files to vector dictionary
    vector_dic = d2v.bins2vectors2dic(file_list)

    # save as bin file
    saver.dictionary2bin(vector_dic)

    end_time = time.time()

    print
    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
    print
