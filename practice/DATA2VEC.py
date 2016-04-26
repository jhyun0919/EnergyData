# -*- coding: utf-8 -*-

# This module gets a directory path as an input argument and
# makes a binary file of vectorized data.

# >>> python DATA2VEC.py <directory>

import time

from utils import Data2Vec
from utils import Load
from utils import Save

if __name__ == "__main__":
    start_time = time.time()



    # get directory path
    abs_path = Load.get_directory()

    # make a list of files from the path
    file_list = Load.load_file(abs_path)

    # convert files to vector dictionary
    vector_dic = Data2Vec.bins2vectors2dic(file_list)

    # save as bin file
    Save.dictionary2bin(abs_path, vector_dic)

    end_time = time.time()

    print
    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
    print
