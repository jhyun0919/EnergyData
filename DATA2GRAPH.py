# -*- coding: utf-8 -*-

import time

from utils import LoadData
from utils import SaveData
from utils import ShowData
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    abs_path = LoadData.get_directory()

    file_list = LoadData.load_file(abs_path)

    # SaveData.bins2graphs(abs_path, file_list)
    ShowData.bins2graphs(abs_path, file_list)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
