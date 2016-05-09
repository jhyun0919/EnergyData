# -*- coding: utf-8 -*-

import os
import cPickle as pickle
from GlobalParameter import *


class Path:
    def __init__(self):
        pass

    @staticmethod
    def path_checker(directory):
        if os.path.isdir(directory):
            return directory
        else:
            directory = directory.rsplit('/', 1)[0]
            Path.path_checker(directory)


class Load:
    def __init__(self):
        pass

    @staticmethod
    def unpickling(binary_file):
        data_dictionary = pickle.load(open(binary_file))

        file_name = binary_file.rsplit('/', 1)[-1]
        file_name = file_name.split('.')[0]
        data_dictionary['file_name'] = file_name

        return data_dictionary

    @staticmethod
    def load_filelist(path):
        bin_file_list = []

        try:
            file_names = os.listdir(path)
            for i in xrange(0, len(file_names)):
                ext = os.path.splitext(file_names[i])[-1]
                if ext == '.bin':
                    file = os.path.join(path, file_names[i])
                    bin_file_list.append(file)
        except OSError as err:
            print 'OSError' + str(err)

        return bin_file_list


class Save:
    def __init__(self):
        pass

    @staticmethod
    def dependency_model2bin_file(dependency_structure):
        path = Repository_Path
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        binary_file_name = path + '/dependency_model.bin'

        f = open(binary_file_name, 'wb')
        pickle.dump(dependency_structure, f, 1)
        f.close()
