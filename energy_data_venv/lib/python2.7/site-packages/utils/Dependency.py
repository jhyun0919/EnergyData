# -*- coding: utf-8 -*-

import numpy as np
from sklearn.neighbors import NearestNeighbors


def cluster2modeldependency(dictionary):
    names = dictionary['file_name']
    vectors = dictionary['vec_data']

    X = np.array(vectors)
    elements = len(X)
    nbrs = NearestNeighbors(n_neighbors=elements, algorithm='auto').fit(X)
    distances, indices = nbrs.kneighbors(X)

    dependency = np.zeros((elements, elements))

    for row in xrange(0, elements):
        for col in xrange(0, elements):
            dependency[row][indices[row][col]] = distances[row][col]

    model_dependency = dependency2dic(names, dependency)

    return model_dependency


def dependency2dic(names, dependency):
    model_dependency = {}
    model_dependency['file_name'] = names
    model_dependency['dependency'] = dependency

    return model_dependency
