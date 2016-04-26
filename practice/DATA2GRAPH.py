# -*- coding: utf-8 -*-

import time

from utils import Load
from utils import Save
from utils import ShowData
from utils.GlobalParam import *

if __name__ == "__main__":
    start_time = time.time()

    abs_path = Load.get_directory()

    file_list = Load.load_file(abs_path)

    # SaveData.bins2graphs(abs_path, file_list)
    ShowData.bins2graphs(abs_path, file_list)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
