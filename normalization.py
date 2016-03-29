import cPickle as pickle
from sklearn import preprocessing
from VEC_03 import normalization, interpolation
import show_graph as g
import types
import numpy as np


file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT/VTT_GW1_HA11_VM_KV_KAM.bin'

tsfile = pickle.load(open(file_path))

# print tsfile

data = interpolation(tsfile)

data.sort()

g.draw_graph(data)


# g.draw_graph(data)
#
# data = normalization(data)
#
# g.draw_graph(data)
#
