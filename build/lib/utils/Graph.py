# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

        plt.title(dictionary['file_name'])
        plt.scatter(x=dictionary['ts'], y=dictionary['value'], color='b', marker='o')
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
        data = FileIO.Load.unpickling(binary_file)
        data['ts'] = data['ts'][:, 0]
        Show.value2graph(data)

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
