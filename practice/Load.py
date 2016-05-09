# # -*- coding: utf-8 -*-
#
# import sys
# import os
# import cPickle as pickle
#
# def unpickling(binary_file):
#     data_dictionary = pickle.load(open(binary_file))
#
#     file_name = binary_file.rsplit('/', 1)[-1]
#     file_name = file_name.split('.')[0]
#     data_dictionary['file_name'] = file_name
#
#     return data_dictionary
#
#
# def load_filelist(path):
#     bin_file_list = []
#
#     try:
#         file_names = os.listdir(path)
#         for i in xrange(0, len(file_names)):
#             ext = os.path.splitext(file_names[i])[-1]
#             if ext == '.bin':
#                 file = os.path.join(path, file_names[i])
#                 bin_file_list.append(file)
#     except OSError as err:
#         print 'OSError' + str(err)
#
#     return bin_file_list