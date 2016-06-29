# -*- coding: utf-8 -*-

from FileIO import Load
from FileIO import Save
from Matrix import symmetric
from Preprocess import ts_synchronize
from GlobalParameter import *
import numpy as np
import os
import time
from math import sqrt
import cPickle as pickle


###############################################################################
# Build Similarity Model

class Build:
    def __init__(self):
        pass

    @staticmethod
    def similarity_model(time_interval=TimeInterval, refine_type=FullyPreprocessedPath):
        data_repository = os.path.join(RepositoryPath, str(time_interval), refine_type)
        model = {}

        model['file_list'] = np.asanyarray(Load.binary_file_list(data_repository))

        for similarity_type in SimilarityType:
            model[similarity_type] = Build.foo(similarity_type, model['file_list'])

        saved_path_model = Save.model2bin_file(data_repository, model)

        return model, saved_path_model

    @staticmethod
    def foo(similarity_type, file_list):

        print 'calculating ' + similarity_type
        start_time = time.time()

        if similarity_type == 'covariance':
            similarity_model = symmetric(SimilarityScore.covariance_model(file_list))
        elif similarity_type == 'cosine_similarity':
            similarity_model = symmetric(SimilarityScore.cosine_similarity_model(file_list))
        elif similarity_type == 'euclidean_distance':
            similarity_model = symmetric(SimilarityScore.euclidean_distance_model(file_list))
        elif similarity_type == 'manhattan_distance':
            similarity_model = symmetric(SimilarityScore.manhattan_distance_model(file_list))
        elif similarity_type == 'gradient_similarity':
            similarity_model = symmetric(SimilarityScore.gradient_similarity_model(file_list))
        elif similarity_type == 'reversed_gradient_similarity':
            similarity_model = symmetric(SimilarityScore.reversed_gradient_similarity_model(file_list))
        else:
            exit()

        # similarity score normalization
        try:
            similarity_model /= similarity_model.std()
        except ZeroDivisionError as err:
            print err
            exit()

        end_time = time.time()
        run_time = end_time - start_time

        print '\t' + 'run_time: ' + str(run_time) + ' sec'

        return similarity_model


###############################################################################
# Cleaning Model

class Clean:
    def __init__(self):
        pass

    @staticmethod
    def overlap(similarity_model, time_interval=TimeInterval):
        # clean similarity model
        overlap_list = Clean.overlap_detection(similarity_model['file_list'])

        for idx in overlap_list:
            similarity_model['file_list'].pop(idx)
            similarity_model['covariance'] = Clean.pop(similarity_model['covariance'], idx)
            similarity_model['cosine_similarity'] = Clean.pop(similarity_model['cosine_similarity'], idx)
            similarity_model['euclidean_distance'] = Clean.pop(similarity_model['euclidean_distance'], idx)
            similarity_model['manhattan_distance'] = Clean.pop(similarity_model['manhattan_distance'], idx)
            similarity_model['gradient_similarity'] = Clean.pop(similarity_model['gradient_similarity'], idx)
            similarity_model['reversed_gradient_similarity'] = Clean.pop(
                similarity_model['reversed_gradient_similarity'], idx)

        saved_path = Save.model2bin_file(similarity_model)

        # clean preprocessed data repository
        overlap_preprocessed_file_list = Clean.diff(
            Load.binary_file_list(os.path.join(RepositoryPath, str(time_interval))), similarity_model['file_list'])
        for file_path in overlap_preprocessed_file_list:
            os.remove(file_path)

        return similarity_model, saved_path

    @staticmethod
    def overlap_detection(detection_target):
        """
        - 중복되는 data 를 찾음

        :param detection_target:
        :return:
        """
        overlap_list = []
        for i in xrange(0, len(detection_target)):
            for j in xrange(i + 1, len(detection_target)):
                if detection_target[i] == detection_target[j]:
                    overlap_list.append(i)

        overlap_list = list(set(overlap_list))
        overlap_list.sort(reverse=True)

        return overlap_list

    @staticmethod
    def pop(matrix, idx):
        """
        - matrix 의 idx-th row & column 을 삭제

        :param matrix:
        :param idx:
        :return:
        """
        del_row = np.delete(matrix, idx, 0)
        del_row_col = np.delete(del_row, np.s_[idx:idx + 1], 1)

        return del_row_col

    @staticmethod
    def diff(old_list, new_list):
        return set(old_list) - set(new_list)


###############################################################################
#

class SimilarityScore:
    def __init__(self):
        pass

    @staticmethod
    def covariance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = SimilarityScore.covariance_score(file_list[row], file_list[col])

        # 오름차순을 위한 어쩔 수 없는 방법
        model = model + abs(model.min())
        model = model.max() - model

        return model

    @staticmethod
    def cosine_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = SimilarityScore.cosine_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def euclidean_distance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = SimilarityScore.euclidean_distance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def manhattan_distance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = SimilarityScore.manhattan_distance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = SimilarityScore.gradient_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def reversed_gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = SimilarityScore.reversed_gradient_similarity_score(file_list[row], file_list[col])

        return model

    ###############################################################################
    # assign similarity score

    @staticmethod
    def covariance_score(binary_file_1, binary_file_2):
        """
        - binary file 의 apb_path 를 받아 두 file data 사이 covariance 를 계산하여 반환
        :param binary_file_1:
            binary file abs_path
            - type: string
        :param binary_file_2:
            binary file ans_path
            - type: string
        :return:
            covariance score
            -type: float
        """
        # early, late, _ = ts_synchronize(binary_file_1, binary_file_2)
        score = SimilarityScore.covariance_calculator(binary_file_1, binary_file_2)

        return score

    @staticmethod
    def cosine_similarity_score(binary_file_1, binary_file_2):
        """
        - binary file 의 apb_path 를 받아 두 file data 사이 cosine similarity 를 계산하여 반환
        :param binary_file_1:
            binary file abs_path
            - type: string
        :param binary_file_2:
            binary file ans_path
            - type: string
        :return:
            cosine similarity score
            -type: float
        """
        # early, late, _ = ts_synchronize(binary_file_1, binary_file_2)
        score = SimilarityScore.cosine_similarity_calculator(binary_file_1, binary_file_2)

        return abs(1 - score)

    @staticmethod
    def euclidean_distance_score(binary_file_1, binary_file_2):
        """
        - binary file 의 apb_path 를 받아 두 file data 사이 euclidean distance 를 계산하여 반환
        :param binary_file_1:
            binary file abs_path
            - type: string
        :param binary_file_2:
            binary file ans_path
            - type: string
        :return:
            euclidean distance score
            -type: float
        """
        # early, late, _ = ts_synchronize(binary_file_1, binary_file_2)
        score = SimilarityScore.euclidean_distance_calculator(binary_file_1, binary_file_2)

        return score

    @staticmethod
    def manhattan_distance_score(binary_file_1, binary_file_2):
        """
        - binary file 의 apb_path 를 받아 두 file data 사이 manhattan distance 를 계산하여 반환
        :param binary_file_1:
            binary file abs_path
            - type: string
        :param binary_file_2:
            binary file ans_path
            - type: string
        :return:
            manhattan distance score
            -type: float
        """
        # early, late, length = ts_synchronize(binary_file_1, binary_file_2)
        score = SimilarityScore.manhattan_distance_calculator(binary_file_1, binary_file_2)

        return score

    @staticmethod
    def gradient_similarity_score(binary_file_1, binary_file_2):
        """
        - binary file 의 apb_path 를 받아 두 file data 사이 gradient similarity 를 계산하여 반환
        :param binary_file_1:
            binary file abs_path
            - type: string
        :param binary_file_2:
            binary file ans_path
            - type: string
        :return:
            gradient similarity score
            -type: float
        """
        # early, late, length = ts_synchronize(binary_file_1, binary_file_2)
        score = SimilarityScore.gradient_similarity_calculator(binary_file_1, binary_file_2)

        return score

    @staticmethod
    def reversed_gradient_similarity_score(binary_file_1, binary_file_2):
        """
        - binary file 의 apb_path 를 받아 두 file data 사이 reversed gradient similarity 를 계산하여 반환
        :param binary_file_1:
            binary file abs_path
            - type: string
        :param binary_file_2:
            binary file ans_path
            - type: string
        :return:
            reversed gradient similarity score
            -type: float
        """
        # early, late, length = ts_synchronize(binary_file_1, binary_file_2)
        score = SimilarityScore.reversed_gradient_similarity_calculator(binary_file_1, binary_file_2)

        return score

    ###############################################################################
    # calculate similarity score

    @staticmethod
    def covariance_calculator(binary_file_1, binary_file_2):
        data_1, data_2 = SimilarityScore.unpickling(binary_file_1, binary_file_2)
        return np.cov(data_1, data_2)[0][1]

    @staticmethod
    def cosine_similarity_calculator(binary_file_1, binary_file_2):
        data_1, data_2 = SimilarityScore.unpickling(binary_file_1, binary_file_2)
        numerator = sum(a * b for a, b in zip(data_1, data_2))
        denominator = SimilarityScore.square_rooted(data_1) * SimilarityScore.square_rooted(data_2)

        return round(numerator / float(denominator), Round)

    @staticmethod
    def euclidean_distance_calculator(binary_file_1, binary_file_2):
        data_1, data_2 = SimilarityScore.unpickling(binary_file_1, binary_file_2)
        return round(sqrt(sum(pow(a - b, 2) for a, b in zip(data_1, data_2))), Round)

    @staticmethod
    def manhattan_distance_calculator(binary_file_1, binary_file_2):
        data_1, data_2 = SimilarityScore.unpickling(binary_file_1, binary_file_2)
        return round(sum(abs(a - b) for a, b in zip(data_1, data_2)), Round)

    @staticmethod
    def gradient_similarity_calculator(binary_file_1, binary_file_2):
        data_1, data_2 = SimilarityScore.unpickling(binary_file_1, binary_file_2)
        score = []

        early_gradient = np.gradient(data_1)
        late_gradient = np.gradient(data_2)

        for a, b, in zip(early_gradient, late_gradient):
            gradient_distance = abs(a - b)
            score.append(gradient_distance)

        return round(sum(score), 3)

    @staticmethod
    def reversed_gradient_similarity_calculator(binary_file_1, binary_file_2):
        data_1, data_2 = SimilarityScore.unpickling(binary_file_1, binary_file_2)
        score = []

        early_gradient = np.gradient(data_1)
        late_gradient = np.gradient(data_2)
        late_gradient = late_gradient

        for a, b, in zip(early_gradient, late_gradient):
            gradient_distance = abs(a - (-b))
            score.append(gradient_distance)

        return round(sum(score), 3)

    @staticmethod
    def square_rooted(x):
        return round(sqrt(sum([a * a for a in x])), Round)

    @staticmethod
    def unpickling(binary_file_1, binary_file_2):
        data_1 = pickle.load(open(binary_file_1))
        data_2 = pickle.load(open(binary_file_2))

        return data_1['value'], data_2['value']


###############################################################################
#

"""
class Extend:
    def __init__(self):
        pass

    ###############################################################################
    # adding similarity column

    @staticmethod
    def add_extra_model(similarity_model_bin_file, data_file):
        model = Load.unpickling(similarity_model_bin_file)
        data_file = Save.preprocessed_data2bin_file(data_preprocess(data_file))

        # file list
        model['file_list'].append(data_file)

        # covariance
        covariance_row, covariance_column = Extend.covariance_column(model['file_list'], data_file)
        model['covariance'] = np.r_[model['covariance'], covariance_row]
        model['covariance'] = np.c_[model['covariance'], covariance_column]

        # cosine similarity
        cosine_row, cosine_column = Extend.cosine_similarity_column(model['file_list'], data_file)
        model['cosine_similarity'] = np.r_[model['cosine_similarity'], cosine_row]
        model['cosine_similarity'] = np.c_[model['cosine_similarity'], cosine_column]

        # euclidean distance
        euclidean_row, euclidean_column = Extend.euclidean_distance_column(model['file_list'], data_file)
        model['euclidean_distance'] = np.r_[model['euclidean_distance'], euclidean_row]
        model['euclidean_distance'] = np.c_[model['euclidean_distance'], euclidean_column]

        # manhattan distance
        manhattan_row, manhattan_column = Extend.manhattan_distance_column(model['file_list'], data_file)
        model['manhattan_distance'] = np.r_[model['manhattan_distance'], manhattan_row]
        model['manhattan_distance'] = np.c_[model['manhattan_distance'], manhattan_column]

        # gradient similarity
        gradient_row, gradient_column = Extend.gradient_similarity_column(model['file_list'], data_file)
        model['gradient_similarity'] = np.r_[model['gradient_similarity'], gradient_row]
        model['gradient_similarity'] = np.c_[model['gradient_similarity'], gradient_column]

        # reversed-gradient similarity
        reversed_gradient_row, reversed_gradient_column = Extend.reversed_gradient_similarity_column(model['file_list'],
                                                                                                     data_file)
        model['reversed_gradient_similarity'] = np.r_[model['reversed_gradient_similarity'], reversed_gradient_row]
        model['reversed_gradient_similarity'] = np.c_[model['reversed_gradient_similarity'], reversed_gradient_column]

        _ = Save.model2bin_file(model)

        return model, data_file

    ###############################################################################
    # build similarity column

    @staticmethod
    def covariance_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = SimilarityScore.covariance_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def cosine_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = SimilarityScore.cosine_similarity_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def euclidean_distance_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = SimilarityScore.euclidean_distance_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def manhattan_distance_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = SimilarityScore.manhattan_distance_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def gradient_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = SimilarityScore.gradient_similarity_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def reversed_gradient_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = SimilarityScore.reversed_gradient_similarity_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column
"""

###############################################################################


if __name__ == '__main__':
    Build.similarity_model()
