# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import FileIO


class Show:
    def __init__(self):
        pass

    @staticmethod
    def dic2graph(dictionary):
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
    def bin2graph(binary_file):
        Show.dic2graph(FileIO.Load.unpickling(binary_file))

    # @staticmethod
    # def bins2graphs(path):
    #     file_list = FileIO.Load.load_filelist(path)
    #     for file in file_list:
    #         Show.bin2graph(file)
    #         print

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


