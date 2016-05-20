# -*- coding: utf-8 -*-

from GlobalParameter import *
from FileIO import Load
from FileIO import Save
from Matrix import decalcomanie
from Preprocess import data_preprocess
# import os
from math import sqrt
from operator import itemgetter
import numpy as np
from Preprocess import preprocess4similarity
import os


class Model:
    def __init__(self):
        pass

    ###############################################################################
    # build similarity model

    @staticmethod
    def build_model(file_list):
        similarity_model = {}

        similarity_model['file_list'] = file_list
        similarity_model['cosine_similarity'] = decalcomanie(Model.cosine_similarity_model(file_list))
        similarity_model['euclidean_distance'] = decalcomanie(Model.euclidean_distance_model(file_list))
        similarity_model['manhattan_distance'] = decalcomanie(Model.manhattan_distance_model(file_list))
        similarity_model['gradient_similarity'] = decalcomanie(Model.gradient_similarity_model(file_list))
        similarity_model['reversed_gradient_similarity'] = decalcomanie(
            Model.reversed_gradient_similarity_model(file_list))

        saved_path = Save.model2bin_file(similarity_model)

        return similarity_model, saved_path

    @staticmethod
    def cosine_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Model.cosine_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def euclidean_distance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Model.euclidean_distance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def manhattan_distance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Model.manhattan_distance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Model.gradient_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def reversed_gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Model.reversed_gradient_similarity_score(file_list[row], file_list[col])

        return model

    ###############################################################################
    # cleaning model

    @staticmethod
    def clean_overlap(similarity_model):
        # clean similarity model
        overlap_list = Model.overlap_detection(similarity_model['file_list'])

        for idx in overlap_list:
            similarity_model['file_list'].pop(idx)
            similarity_model['cosine_similarity'] = Model.pop_row_column(similarity_model['cosine_similarity'], idx)
            similarity_model['euclidean_distance'] = Model.pop_row_column(similarity_model['euclidean_distance'], idx)
            similarity_model['manhattan_distance'] = Model.pop_row_column(similarity_model['manhattan_distance'], idx)
            similarity_model['gradient_similarity'] = Model.pop_row_column(similarity_model['gradient_similarity'], idx)
            similarity_model['reversed_gradient_similarity'] = Model.pop_row_column(
                similarity_model['reversed_gradient_similarity'], idx)

        saved_path = Save.model2bin_file(similarity_model)

        # clean preprocessed data repository
        old_preprocessed_file_list = Load.load_filelist(os.path.join(Repository_Path, Preprocessed_Path))
        overlap_preprocessed_file_list = Model.diff(old_preprocessed_file_list, similarity_model['file_list'])

        for file_path in overlap_preprocessed_file_list:
            os.remove(file_path)

        return similarity_model, saved_path

    @staticmethod
    def overlap_detection(detection_target):
        overlap_list = []
        for i in xrange(0, len(detection_target)):
            for j in xrange(i + 1, len(detection_target)):
                if detection_target[i] == detection_target[j]:
                    overlap_list.append(i)

        overlap_list = list(set(overlap_list))
        overlap_list.sort(reverse=True)

        return overlap_list

    @staticmethod
    def pop_row_column(matrix, idx):
        del_row = np.delete(matrix, idx, 0)
        del_row_col = np.delete(del_row, np.s_[idx:idx + 1], 1)

        return del_row_col

    @staticmethod
    def diff(list_a, list_b):
        list_b = set(list_b)
        return [item for item in list_a if item not in list_b]

    ###############################################################################
    # adding similarity column

    @staticmethod
    def add_extra_model(similarity_model_bin_file, data_file):
        model = Load.unpickling(similarity_model_bin_file)
        data_file = Save.preprocessed_data2bin_file(data_preprocess(data_file))

        # cosine similarity column
        cosine_column = Model.cosine_similarity_column(model['file_list'], data_file)
        cosine_row = Model.build_extra_row(cosine_column)
        cosine_model = np.c_[model['cosine_similarity'], cosine_column]
        cosine_model = np.r_[cosine_model, cosine_row]
        model['cosine_similarity'] = cosine_model

        # euclidean distance column
        euclidean_column = Model.euclidean_distance_column(model['file_list'], data_file)
        euclidean_row = Model.build_extra_row(euclidean_column)
        euclidean_model = np.c_[model['euclidean_distance'], euclidean_column]
        euclidean_model = np.r_[euclidean_model, euclidean_row]
        model['euclidean_distance'] = euclidean_model

        # manhattan distance column
        manhattan_column = Model.manhattan_distance_column(model['file_list'], data_file)
        manhattan_row = Model.build_extra_row(manhattan_column)
        manhattan_model = np.c_[model['manhattan_distance'], manhattan_column]
        manhattan_model = np.r_[manhattan_model, manhattan_row]
        model['manhattan_distance'] = manhattan_model

        # gradient similarity column
        gradient_column = Model.gradient_similarity_column(model['file_list'], data_file)
        gradient_row = Model.build_extra_row(gradient_column)
        gradient_model = np.c_[model['gradient_similarity'], gradient_column]
        gradient_model = np.r_[gradient_model, gradient_row]
        model['gradient_similarity'] = gradient_model

        # reversed-gradient similarity column
        reversed_gradient_column = Model.reversed_gradient_similarity_column(model['file_list'], data_file)
        reversed_gradient_row = Model.build_extra_row(reversed_gradient_column)
        reversed_gradient_model = np.c_[model['reversed_gradient_similarity'], reversed_gradient_column]
        reversed_gradient_model = np.r_[reversed_gradient_model, reversed_gradient_row]
        model['reversed_gradient_similarity'] = reversed_gradient_model

        # file list
        model['file_list'].append(data_file)

        _ = Save.model2bin_file(model)

        return model, data_file

    @staticmethod
    def build_extra_row(extra_column):
        extra_row = np.transpose(extra_column)
        extra_row = np.c_[extra_row, [np.zeros(1)]]

        return extra_row

    ###############################################################################
    # build similarity column

    @staticmethod
    def cosine_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.cosine_similarity_score(file_list[row], data_file)

        return column

    @staticmethod
    def euclidean_distance_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.euclidean_distance_score(file_list[row], data_file)

        return column

    @staticmethod
    def manhattan_distance_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.manhattan_distance_score(file_list[row], data_file)

        return column

    @staticmethod
    def gradient_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.gradient_similarity_score(file_list[row], data_file)

        return column

    @staticmethod
    def reversed_gradient_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.reversed_gradient_similarity_score(file_list[row], data_file)

        return column

    ###############################################################################
    # assign similarity score

    @staticmethod
    def cosine_similarity_score(binary_file_1, binary_file_2):
        early, late, _ = preprocess4similarity(binary_file_1, binary_file_2)
        score = Model.cosine_similarity_calculator(early, late)

        if score >= 0:
            score = 1 - score
        else:
            score = -1 - score

        return score

    @staticmethod
    def euclidean_distance_score(binary_file_1, binary_file_2):
        early, late, _ = preprocess4similarity(binary_file_1, binary_file_2)
        score = Model.euclidean_distance_calculator(early, late)
        return score

    @staticmethod
    def manhattan_distance_score(binary_file_1, binary_file_2):
        early, late, length = preprocess4similarity(binary_file_1, binary_file_2)
        score = Model.manhattan_distance_calculator(early, late)
        return score / length

    @staticmethod
    def gradient_similarity_score(binary_file_1, binary_file_2):
        early, late, length = preprocess4similarity(binary_file_1, binary_file_2)
        score = Model.gradient_similarity_calculator(early, late)
        return score / length

    @staticmethod
    def reversed_gradient_similarity_score(binary_file_1, binary_file_2):
        early, late, length = preprocess4similarity(binary_file_1, binary_file_2)
        score = Model.reversed_gradient_similarity_calculator(early, late)
        return score / length

    ###############################################################################
    # calculate similarity score

    @staticmethod
    def cosine_similarity_calculator(early, late):
        numerator = sum(a * b for a, b in zip(early, late))
        denominator = Model.square_rooted(early) * Model.square_rooted(late)
        return round(numerator / float(denominator), Round)

    @staticmethod
    def euclidean_distance_calculator(early, late):
        return round(sqrt(sum(pow(a - b, 2) for a, b in zip(early, late))), Round)

    @staticmethod
    def manhattan_distance_calculator(early, late):
        return round(sum(abs(a - b) for a, b in zip(early, late)), Round)

    @staticmethod
    def gradient_similarity_calculator(early, late):
        score = []

        early_gradient = np.gradient(early)
        late_gradient = np.gradient(late)

        for a, b, in zip(early_gradient, late_gradient):
            gradient_distance = abs(a - b)
            # if gradient_distance < Gradient_Threshold:
            #     score.append(0)
            # else:
            #
            score.append(gradient_distance)

        return round(sum(score), 3)

    @staticmethod
    def reversed_gradient_similarity_calculator(early, late):
        score = []

        early_gradient = np.gradient(early)
        late_gradient = np.gradient(late)
        late_gradient = late_gradient

        for a, b, in zip(early_gradient, late_gradient):
            gradient_distance = abs(a - (-b))
            # if gradient_distance < Gradient_Threshold:
            #     score.append(0)
            # else:
            #     score.append(gradient_distance)
            score.append(gradient_distance)

        return round(sum(score), 3)

    @staticmethod
    def square_rooted(x):
        return round(sqrt(sum([a * a for a in x])), Round)


class Report:
    def __init__(self):
        pass

    ###############################################################################
    # ordering algorithm

    @staticmethod
    def pick_column(similarity_model_bin_file, data_file):
        model = Load.unpickling(similarity_model_bin_file)

        try:
            idx = model['file_list'].index(data_file)
        except ValueError as err:
            print err
            exit()

        target_column_model = {}

        target_column_model['file_list'] = model['file_list']
        target_column_model['cosine_similarity'] = model['cosine_similarity'][idx]
        target_column_model['euclidean_distance'] = model['euclidean_distance'][idx]
        target_column_model['manhattan_distance'] = model['manhattan_distance'][idx]
        target_column_model['gradient_similarity'] = model['gradient_similarity'][idx]
        target_column_model['reversed_gradient_similarity'] = model['reversed_gradient_similarity'][idx]

        return target_column_model

    @staticmethod
    def sorting_column(target_column_model):
        cosine_sorting_column = Report.sorting_tuples_list(
            Report.binder(target_column_model['cosine_similarity'],
                          target_column_model['file_list']))
        euclidean_sorting_column = Report.sorting_tuples_list(
            Report.binder(target_column_model['euclidean_distance'],
                          target_column_model['file_list']))
        manhattan_sorting_column = Report.sorting_tuples_list(
            Report.binder(target_column_model['manhattan_distance'],
                          target_column_model['file_list']))
        gradient_sorting_column = Report.sorting_tuples_list(
            Report.binder(target_column_model['gradient_similarity'],
                          target_column_model['file_list']))
        r_gradient_sorting_column = Report.sorting_tuples_list(
            Report.binder(target_column_model['reversed_gradient_similarity'],
                          target_column_model['file_list']))

        sorted_column_model = {}

        sorted_column_model['cosine_similarity'] = cosine_sorting_column
        sorted_column_model['euclidean_distance'] = euclidean_sorting_column
        sorted_column_model['manhattan_distance'] = manhattan_sorting_column
        sorted_column_model['gradient_similarity'] = gradient_sorting_column
        sorted_column_model['reversed_gradient_similarity'] = r_gradient_sorting_column

        return sorted_column_model

    @staticmethod
    def binder(similarity, file_list):
        tuples_list = []

        for a, b in zip(similarity, file_list):
            item = (b, a)
            tuples_list.append(item)

        return tuples_list

    @staticmethod
    def sorting_tuples_list(tuples_list):
        tuples_list.sort(key=itemgetter(1))

        return tuples_list


class Network():
    def __init__(self):
        pass

    @staticmethod
    def build_network(similarity_model):
        pass


###############################################################################


if __name__ == '__main__':
    path = os.path.join(Repository_Path, Preprocessed_Path)
    file_list = Load.load_filelist(path)

    # for file in file_list:
    #     print file

    similarity_model, _ = Model.build_model(file_list)

    # print similarity_model['euclidean_distance']
    # print similarity_model['cosine_similarity']
    # print similarity_model['gradient_similarity']
    # print similarity_model['reversed_gradient_similarity']

    # similarity_model = Load.unpickling(
    #     '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/model/model.bin')

    # similarity_model, added_file_name = Model.add_extra_model(
    #     '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/model/model.bin',
    #     '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/VTT_GW2_HA7_VM_EP_KV_K.bin')
    #
    # print added_file_name
    # print

    # for line in similarity_model['file_list']:
    #     print line

    # similarity_model, _ = Model.clean_overlap(similarity_model)

    # print similarity_model

    # for line in similarity_model['file_list']:
    #     print line

    print similarity_model

    # added_file_name = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/preprocessed_data/PP_VTT_GW2_HA7_VM_EP_KV_K.bin'

    # target_column_model = Report.pick_column(
    #     '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/model/model.bin', added_file_name)
    # print target_column_model

    # sorted_column_model = Report.sorting_column(target_column_model)
    # print sorted_column_model
    # print
    # for line in sorted_column_model['cosine_similarity']:
    #     print line
    # print
    # for line in sorted_column_model['euclidean_distance']:
    #     print line
    # print
    # for line in sorted_column_model['gradient_similarity']:
    #     print line
    # print
    # for line in sorted_column_model['reversed_gradient_similarity']:
    #     print line
    # print
