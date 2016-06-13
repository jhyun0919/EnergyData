# -*- coding: utf-8 -*-


from FileIO import Load
from FileIO import Save
from GlobalParameter import *
import os

import numpy as np
import matplotlib.pyplot as plt

try:
    from matplotlib.finance import quotes_historical_yahoo
except ImportError:
    from matplotlib.finance import quotes_historical_yahoo_ochl as quotes_historical_yahoo
from matplotlib.collections import LineCollection

from sklearn import cluster, covariance, manifold


###############################################################################
# preprocess

class Preprocess:
    def __init__(self):
        pass

    @staticmethod
    def preprocess4network(file_list):
        # ts start & end 임시 배정
        file = Load.unpickling(file_list[0])
        latest_start_ts = file['ts'][0]
        earliest_ent_ts = file['ts'][-1]

        # search ts start & end
        for line in file_list:
            line = Load.unpickling(line)
            if line['ts'][0] > latest_start_ts:
                latest_start_ts = line['ts'][0]
            if line['ts'][-1] < earliest_ent_ts:
                earliest_ent_ts = line['ts'][-1]

        names = Preprocess.name_setter(file_list)

        for file, name, in zip(file_list, names):
            data_dictionary = {}
            data_dictionary['file_name'] = name
            data_dictionary['value'] = Preprocess.data_extractor(file, latest_start_ts, earliest_ent_ts)
            Save.network_data2bin_file(data_dictionary)

    @staticmethod
    def data_extractor(file, start_ts, end_ts):
        file = Load.unpickling(file)

        for i in xrange(0, len(file['ts'])):
            if file['ts'][i] == start_ts:
                start_idx = i
                break
        for j in xrange(1, len(file['ts'])):
            if file['ts'][-j] == end_ts:
                end_idx = -j
                break

        return file['value'][start_idx:end_idx]

    @staticmethod
    def value_setter():
        values = []

        path = os.path.join(Repository_Path, Network_Path)
        file_list = Load.load_filelist(path)

        for file in file_list:
            data = Load.unpickling(file)
            values.append(data['value'])

        return np.array(values)

    @staticmethod
    def gradient_setter(file_list):
        gradients = []

        for file in file_list:
            gradients.append(np.gradient(file['value']))

        return gradients

    @staticmethod
    def name_setter(file_list):
        names = []

        for file in file_list:
            file = file.rsplit('/', 1)[-1]
            file = file.split('.')[0]
            file = file.split('_', 2)[-1]
            names.append(file)

        return names


###############################################################################
# build network

class Show:
    def __init__(self):
        pass

    @staticmethod
    def value_network(file_list):
        Preprocess.preprocess4network(file_list)

        names = Preprocess.name_setter(file_list)

        values = Preprocess.value_setter()

        for name, data, in zip(names, values):
            print name
            print data
            print data.shape

        Show.build_network(values, names)

    @staticmethod
    def gadient_network(file_list):
        Preprocess.preprocess4network(file_list)

        names = Preprocess.name_setter(file_list)

        gradients = Preprocess.gradient_setter()

        Show.build_network(gradients, names)

    @staticmethod
    def build_network(variation, names):
        ###############################################################################
        # Learn a graphical structure from the correlations
        edge_model = covariance.GraphLassoCV()

        # standardize the time series: using correlations rather than covariance
        # is more efficient for structure recovery
        X = variation.copy().T
        X /= X.std(axis=0)
        edge_model.fit(X)

        ###############################################################################
        # Cluster using affinity propagation

        _, labels = cluster.affinity_propagation(edge_model.covariance_)
        n_labels = labels.max()

        for i in range(n_labels + 1):
            print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))

        ###############################################################################
        # Find a low-dimension embedding for visualization: find the best position of
        # the nodes (the stocks) on a 2D plane

        # We use a dense eigen_solver to achieve reproducibility (arpack is
        # initiated with random vectors that we don't control). In addition, we
        # use a large number of neighbors to capture the large-scale structure.
        node_position_model = manifold.LocallyLinearEmbedding(n_components=2, eigen_solver='dense', n_neighbors=6)

        embedding = node_position_model.fit_transform(X.T).T

        ###############################################################################
        # Visualization
        plt.figure(1, facecolor='w', figsize=(10, 8))
        plt.clf()
        ax = plt.axes([0., 0., 1., 1.])
        plt.axis('off')

        # Display a graph of the partial correlations
        partial_correlations = edge_model.precision_.copy()
        d = 1 / np.sqrt(np.diag(partial_correlations))
        partial_correlations *= d
        partial_correlations *= d[:, np.newaxis]
        non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)

        # Plot the nodes using the coordinates of our embedding
        plt.scatter(embedding[0], embedding[1], s=100 * d ** 2, c=labels, cmap=plt.cm.spectral)

        # Plot the edges
        start_idx, end_idx = np.where(non_zero)
        # a sequence of (*line0*, *line1*, *line2*), where::
        #            linen = (x0, y0), (x1, y1), ... (xm, ym)
        segments = [[embedding[:, start], embedding[:, stop]]
                    for start, stop in zip(start_idx, end_idx)]
        values = np.abs(partial_correlations[non_zero])
        lc = LineCollection(segments, zorder=0, cmap=plt.cm.hot_r, norm=plt.Normalize(0, .7 * values.max()))
        lc.set_array(values)
        lc.set_linewidths(15 * values)
        ax.add_collection(lc)

        # Add a label to each node. The challenge here is that we want to
        # position the labels to avoid overlap with other labels
        for index, (name, label, (x, y)) in enumerate(zip(names, labels, embedding.T)):

            dx = x - embedding[0]
            dx[index] = 1
            dy = y - embedding[1]
            dy[index] = 1
            this_dx = dx[np.argmin(np.abs(dy))]
            this_dy = dy[np.argmin(np.abs(dx))]
            if this_dx > 0:
                horizontal_alignment = 'left'
                x += .002
            else:
                horizontal_alignment = 'right'
                x -= .002
            if this_dy > 0:
                vertical_alignment = 'bottom'
                y += .002
            else:
                vertical_alignment = 'top'
                y -= .002
            plt.text(x, y, name, size=10,
                     horizontalalignment=horizontal_alignment,
                     verticalalignment=vertical_alignment,
                     bbox=dict(facecolor='w',
                               edgecolor=plt.cm.spectral(label / float(n_labels)),
                               alpha=.6))

        plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),
                 embedding[0].max() + .10 * embedding[0].ptp(), )
        plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),
                 embedding[1].max() + .03 * embedding[1].ptp())

        plt.show()




        ###############################################################################


if __name__ == '__main__':
    path = os.path.join(Repository_Path, Preprocessed_Path)
    file_list = Load.load_filelist(path)

    Show.value_network(file_list)
