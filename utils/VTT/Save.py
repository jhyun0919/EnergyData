# -*- coding: utf-8 -*-

import os
import cPickle as pickle

def dependency_model2bin_file(dependency_structure):

    

    f = open(bin_file, 'wb')
    pickle.dump(dependency_structure, f, 1)
    f.close()