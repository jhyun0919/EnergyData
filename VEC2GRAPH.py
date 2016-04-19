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

    vectors = loader.unpickling(dir_name)

    saver.vectors2graphs(vectors)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
