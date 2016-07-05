# -*- coding: utf-8 -*-

from utils.FileIO import Load
import cPickle as pickle

data_repository_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/VTT'
file_list = Load.binary_file_list(data_repository_path)

for file in file_list:
    data = pickle.load(open(file))
    try:
        print data['ts'][0][0],
        print '\t',
        print data['ts'][-1][0]
    except TypeError:
        print data['ts'][0],
        print '\t',
        print data['ts'][-1]