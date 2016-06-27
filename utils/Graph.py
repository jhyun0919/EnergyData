# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import FileIO
import os
import time
from GlobalParameter import *


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


class Save:
    def __init__(self):
        pass

    @staticmethod
    def raw_data2graph(directory):
        save_path = os.path.join(Repository_Path, Graph_path)
        FileIO.Save.assure_path_exist(save_path)

        for binary_file in FileIO.Load.load_binary_file_list(directory):
            # load data
            dictionary = FileIO.Load.unpickling(binary_file)

            print 'drawing : ',
            print dictionary['file_name']
            start_time = time.time()

            # make a plot
            plt.title(dictionary['file_name'])
            plt.scatter(x=dictionary['ts'][:, 0], y=dictionary['value'], color='b', marker='o')

            # save it in png formats
            graph_figure_path = os.path.join(save_path, dictionary['file_name'] + '.png')
            plt.savefig(graph_figure_path, format='png')
            plt.close()

            end_time = time.time()
            run_time = end_time - start_time
            print '\t' + 'run_time: ' + str(run_time) + ' sec'
