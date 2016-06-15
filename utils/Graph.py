# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import FileIO


###############################################################################
# Show Graph

class Show:
    def __init__(self):
        pass

    @staticmethod
    def value2graph(dictionary):
        """

        :param dictionary:
        :return:
        """
        x = []
        for ts in dictionary['ts']:
            try:
                x.append(ts[0])
            except TypeError:
                x.append(ts)

        y = dictionary['value']

        plt.title(dictionary['file_name'])
        plt.scatter(x, y, marker='x')
        plt.show()
        plt.close()

    @staticmethod
    def instant_value2graph(dictionary):
        """

        :param dictionary:
        :return:
        """
        x = []
        for ts in dictionary['ts']:
            try:
                x.append(ts[0])
            except TypeError:
                x.append(ts)

        y = dictionary['instantaneous_value']

        plt.title(dictionary['file_name'])
        plt.scatter(x, y, marker='x')
        plt.show()
        plt.close()

    @staticmethod
    def bin2graph(binary_file):
        """
        -
        :param binary_file:
            energy data에 해당하는 bainary file
        :return:
            NA
        """
        Show.value2graph(FileIO.Load.unpickling(binary_file))

    @staticmethod
    def vectors2graphs(file):
        """

        :param file:
        :return:
        """
        vectors = FileIO.Load.unpickling(file)
        for i in xrange(len(vectors['file_name'])):
            name = vectors['file_name'][i].rsplit('/', 1)[1]
            name = name.split('.')[0]

            x = np.linspace(0, 1, len(vectors['vec_data'][i]))
            plt.scatter(x, vectors['vec_data'][i], marker='+')
            plt.title(name)
            plt.show()
            plt.close()
            print
