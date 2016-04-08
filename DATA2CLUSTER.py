# -*- coding: utf-8 -*-

from VEC2CLUSTER import*

VEC_DIMENSION = 50
INTERPOLATION_INTERVAL = 10  # minute
SCALE_SIZE = 100
AF_PREFERENCE = -5000

if __name__ == "__main__":
    start_time = time.time()

    dir_name = get_directory()
    file_list = load_file(dir_name)
    vector_dic = bins2vectors2dic(file_list)
    cluster = affinity_propagation(vector_dic)

    print cluster

    clustered_graph(vector_dic['file_name'], cluster)


    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'