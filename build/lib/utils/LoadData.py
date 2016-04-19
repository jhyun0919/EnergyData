# -*- coding: utf-8 -*-

import sys
import os
import cPickle as pickle


# 절대경로나 외부인자를 입력
#
def get_directory(dir_name=None):
    if dir_name is None:
        try:
            dir_name = sys.argv[1]
            if dir_name[0] == '.':
                dir_name = dir_name[1:]
                if dir_name[0] == '/':
                    dir_name = dir_name[1:]

            dir_name = os.path.join(os.getcwd(), dir_name)
            return dir_name
        except IndexError as err:
            print('IndexError: ' + str(err))
            print('Put a directory path as an input argument')
            exit()
    else:
        return dir_name


# directory를 입력받아
# 그 디렉토리 내 binary file들의 절대경로를
# list로 만들어 반환
def load_file(path):
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


# binary file을 unpickling 처리하여
# 읽어옴
def unpickling(bin_file):
    data = pickle.load(open(bin_file))
    return data
