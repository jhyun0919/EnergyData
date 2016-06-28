# -*- coding: utf-8 -*-

import os
import cPickle as pickle
from GlobalParameter import *


###############################################################################
# Load File

class Load:
    def __init__(self):
        pass

    @staticmethod
    def unpickling(binary_file):
        """

        :param binary_file:
        :return:
        """
        data_dictionary = pickle.load(open(binary_file))

        file_name = binary_file.rsplit('/', 1)[-1]
        file_name = file_name.split('.')[0]
        data_dictionary['file_name'] = file_name

        return data_dictionary

    @staticmethod
    def binary_file_list(directory):
        """
        - directory 내에 있는 binary file 들의 abs_path 를 list 로 만들어 반환함

        :param directory:
            directory
        :return:
            binary file list
            - type: list
        """
        bin_file_list = []

        try:
            file_names = os.listdir(directory)
            for i in xrange(0, len(file_names)):
                ext = os.path.splitext(file_names[i])[-1]
                if ext == '.bin':
                    file = os.path.join(directory, file_names[i])
                    bin_file_list.append(file)
        except OSError as err:
            print 'OSError' + str(err)
            exit()

        if len(bin_file_list) == 0:
            print 'There is no binary file in the given directory path'
            exit()

        return bin_file_list

    @staticmethod
    def print_dictionary(data_dictionary):
        """

        :param data_dictionary:
        :return:
        """
        for i in xrange(0, len(data_dictionary['ts'])):
            print data_dictionary['ts'][i],
            print '\t',
            print data_dictionary['value'][i]


###############################################################################
# Save File

class Save:
    def __init__(self):
        pass

    @staticmethod
    def assure_path_exist(path):
        """

        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

    @staticmethod
    def dumping_bin(path, data):
        """

        :param path:
        :param data:
        :return:
        """
        f = open(path, 'wb')
        pickle.dump(data, f, 1)
        f.close()

    @staticmethod
    def refined_data2bin_file(refined_data, save_directory, time_interval=Time_Interval):
        """

        :param refined_data:
        :param time_interval:
        :param save_directory:
        :return:
        """
        path = os.path.join(Repository_Path, str(time_interval), save_directory)
        Save.assure_path_exist(path)

        refined_data_binary_file_name = refined_data['file_name'] + '.bin'
        refined_data_binary_file_name = os.path.join(path, refined_data_binary_file_name)
        Save.dumping_bin(refined_data_binary_file_name, refined_data)

        return refined_data_binary_file_name, path

    @staticmethod
    def model2bin_file(directory, similarity_structure):

        path = os.path.join(directory, Model_Path)
        Save.assure_path_exist(path)

        model_binary_file_name = 'similarity.bin'
        model_binary_file_name = os.path.join(path, model_binary_file_name)

        Save.dumping_bin(model_binary_file_name, similarity_structure)

        return model_binary_file_name

    @staticmethod
    def network_data2bin_file(data_dictionary):
        """

        :param data_dictionary:
        :return:
        """
        path = os.path.join(Repository_Path, Network_Path)

        Save.assure_path_exist(path)

        preprocessed_binary_file_name = 'N_' + data_dictionary['file_name'] + '.bin'
        preprocessed_binary_file_name = os.path.join(path, preprocessed_binary_file_name)

        Save.dumping_bin(preprocessed_binary_file_name, data_dictionary)

        return preprocessed_binary_file_name
