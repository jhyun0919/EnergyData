# -*- coding: utf-8 -*-

import sys
import os
import cPickle as pickle

def unpickling(binary_file):
    data = pickle.load(open(binary_file))
    return data