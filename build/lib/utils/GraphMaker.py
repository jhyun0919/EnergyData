# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
from LoadData import unpickling
from GlobalParam import *


class Graph:
    def __init__(self):
        pass

    class Show:
        @staticmethod
        def bin2graph(file):
            x = []
            for line in unpickling(file)['ts']:
                x.append(line[0])
            y = unpickling(file)['value']

            file_name = file.rsplit('/', 1)[-1]
            file_name = file_name.split('.')[0] + '.jpg'

            plt.title(file_name)
            plt.scatter(x, y, marker='x')

        @staticmethod
        def bins2graphs(file_list):
            for file in file_list:
                x = []
                for line in unpickling(file)['ts']:
                    x.append(line[0])
                y = unpickling(file)['value']

                plt.scatter(x, y, marker='x')

                file_name = file.rsplit('/', 1)[1]
                file_name = file_name.split('.')[0] + '.jpg'

                plt.title(file_name)
                plt.show()
                plt.close()
                print

    class Save:
        def __init__(self):
            pass

        @staticmethod
        def bin2graph(file):
            x = []
            for line in unpickling(file)['ts']:
                x.append(line[0])
            y = unpickling(file)['value']

            file_name = file.rsplit('/', 1)[-1]
            file_name = file_name.split('.')[0] + '.jpg'

            plt.title(file_name)
            plt.scatter(x, y, marker='x')

        @staticmethod
        def bins2graphs(path, file_list):
            old_path = os.getcwd()

            path = os.path.join(path, RESULT_DIRECTORY, 'graph')
            if not os.path.exists(path):
                os.makedirs(path)
            os.chdir(path)

            for file in file_list:
                x = []
                for line in unpickling(file)['ts']:
                    x.append(line[0])
                y = unpickling(file)['value']

                file_name = file.rsplit('/', 1)[1]
                file_name = file_name.split('.')[0] + '.jpg'

                plt.title(file_name)
                plt.scatter(x, y, marker='x')
                plt.savefig(file_name)
                plt.close()

            os.chdir(old_path)
