# -*- coding: utf-8 -*-

import numpy as np


def symmetric(matrix):
    shape = matrix.shape
    if shape[0] == shape[1]:
        symmetric_matrix = matrix + matrix.T - np.diag(matrix.diagonal())
    else:
        print 'given matrix is not squared matrix'
        exit()

    return symmetric_matrix
