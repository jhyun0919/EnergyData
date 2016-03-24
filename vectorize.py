#-*- coding: utf-8 -*-

import sys
import cPickle as pickle
import copy



# Load Data

try:
    #file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT/VTT_GW1_HA2_VM_EP_KV_K.bin'
    file_path = sys.argv[1]
except IndexError as err:
    print('IndexError: ' + str(err))
    print('Usage: python parsing <filename>')
    exit()

data = pickle.load(open(file_path))
time_stamp = data['ts']
value = data['value']

