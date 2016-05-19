# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from FileIO import Load
from GlobalParameter import *
from Similarity import Report


###############################################################################
# build network

def build_network():
    pass


###############################################################################

if __name__ == '__main__':
    similarity_model = Load.unpickling(
        '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/model/model.bin')
    added_file_name = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/preprocessed_data/PP_VTT_GW2_HA7_VM_EP_KV_K.bin'

    target_column_model = Report.pick_column(
        '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/model/model.bin', added_file_name)

    sorted_column_model = Report.sorting_column(target_column_model)

    for line in sorted_column_model['cosine_similarity']:
        print line
