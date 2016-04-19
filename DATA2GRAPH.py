# -*- coding: utf-8 -*-

import time

from utils import LoadData
from utils import SaveData
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    loader = LoadData()
    saver = SaveData(RESULT_DIRECTORY, VEC_DIMENSION)

    dir_name = loader.get_directory()

    file_list = loader.load_file(dir_name)

    saver.bins2graphs(file_list)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
