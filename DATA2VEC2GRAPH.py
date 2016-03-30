# -*- coding: utf-8 -*-

from VEC2GRAPH import *


# main function
if __name__ == "__main__":
    start_time = time.time()

    dir_name = get_directory()

    file_list = load_file(dir_name)

    vector_dic = vector2dic(file_list)

    vector2graph(vector_dic)

    end_time = time.time()

    print
    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'

