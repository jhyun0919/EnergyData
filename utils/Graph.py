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
    def dictionary2graph(dictionary):
        """

        :param dictionary:
        :return:
        """

        plt.title(dictionary['file_name'])
        plt.scatter(x=dictionary['ts'], y=dictionary['value'], color='b', marker='o')
        plt.show()
        plt.close()

    @staticmethod
    def raw_data2graph(binary_file):
        """
        -
        :param binary_file:
            energy data에 해당하는 bainary file
        :return:
            NA
        """
        data = FileIO.Load.unpickling(binary_file)
        data['ts'] = data['ts'][:, 0]
        Show.dictionary2graph(data)

    @staticmethod
    def refined_data2graph(binary_file):
        """

        :param binary_file:
        :return:
        """
        Show.dictionary2graph(FileIO.Load.unpickling(binary_file))
    """
    @staticmethod
    def vectors2graphs(file):

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
    """