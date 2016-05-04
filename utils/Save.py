# -*- coding: utf-8 -*-

import os
import cPickle as pickle
from GlobalParameter import *


def dependency_model2bin_file(dependency_structure):
    path = Repository_Path
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    binary_file_name = path + '/dependency_model.bin'

    f = open(binary_file_name, 'wb')
    pickle.dump(dependency_structure, f, 1)
    f.close()
