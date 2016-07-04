# -*- coding: utf-8 -*-
from FileIO import Load
from GlobalParameter import *
import os
import cPickle as pickle
from sklearn.cluster import AffinityPropagation
import numpy as np
from sklearn.manifold import TSNE


class AffinityProp:
    def __init__(self):
        pass

    @staticmethod
    def build_cluster(time_interval=TimeInterval, refined_type=FullyPreprocessedPath, covariance=True,
                      cosine_similarity=True, euclidean_distance=False, manhattan_distance=False,
                      gradient_similarity=False, reversed_gradient_similarity=False):
        print 'affinity propagation clusters'

        path = os.path.join(RepositoryPath, str(time_interval), refined_type, ModelPath)
        binary_files = Load.binary_file_list(path)

        similarity_model = pickle.load(open(binary_files[0]))

        generate_data(similarity_model, covariance, cosine_similarity, euclidean_distance, manhattan_distance,
                      gradient_similarity,
                      reversed_gradient_similarity)

        X = generate_data(similarity_model, covariance, cosine_similarity, euclidean_distance, manhattan_distance,
                          gradient_similarity, reversed_gradient_similarity)

        af = AffinityPropagation(preference=AffinityPreference).fit(X)
        cluster_centers_indices = af.cluster_centers_indices_
        labels = af.labels_

        n_clusters_ = len(cluster_centers_indices)

        print '\t',
        print('estimated number of clusters: %d' % n_clusters_)

        for i in xrange(len(similarity_model['file_list'])):
            similarity_model['file_list'][i] = similarity_model['file_list'][i].rsplit('/', 1)[-1]

        for i in xrange(0, n_clusters_):
            print '\t',
            print('cluster %i: %s' % ((i + 1), ', '.join(similarity_model['file_list'][labels == i])))


def generate_data(model, covariance=True, cosine_similarity=True, euclidean_distance=True, manhattan_distance=True,
                  gradient_similarity=True, reversed_gradient_similarity=False):
    X = []
    for i in xrange(0, len(model['file_list'])):
        x = []

        if covariance:
            x.append(model['covariance'][0][i])
        if cosine_similarity:
            x.append(model['cosine_similarity'][0][i])
        if euclidean_distance:
            x.append(model['euclidean_distance'][0][i])
        if manhattan_distance:
            x.append(model['manhattan_distance'][0][i])
        if gradient_similarity:
            x.append(model['gradient_similarity'][0][i])
        if reversed_gradient_similarity:
            x.append(model['reversed_gradient_similarity'][0][i])

        X.append(x)

    return X


if __name__ == '__main__':
    AffinityProp.build_cluster()
