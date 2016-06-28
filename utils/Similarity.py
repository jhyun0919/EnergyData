# -*- coding: utf-8 -*-

from FileIO import Load
from FileIO import Save
from Matrix import symmetric
import numpy as np
import os
from GlobalParameter import Repository_Path


###############################################################################
# Build Similarity Model
class Model:
    def __init__(self):
        pass

    @staticmethod
    def build(data_repository):
        similarity_model = {}

        similarity_model['file_list'] = np.asanyarray(Load.binary_file_list(data_repository))
        similarity_model['covariance'] = symmetric(SimilarityScore.covariance_model(similarity_model['file_list']))
        similarity_model['cosine_similarity'] = symmetric(
            SimilarityScore.cosine_similarity_model(similarity_model['file_list']))
        similarity_model['euclidean_distance'] = symmetric(
            SimilarityScore.euclidean_distance_model(similarity_model['file_list']))
        similarity_model['manhattan_distance'] = symmetric(
            SimilarityScore.manhattan_distance_model(similarity_model['file_list']))
        similarity_model['gradient_similarity'] = symmetric(
            SimilarityScore.gradient_similarity_model(similarity_model['file_list']))
        similarity_model['reversed_gradient_similarity'] = symmetric(
            SimilarityScore.reversed_gradient_similarity_model(similarity_model['file_list']))

        saved_path_similarity_model = Save.model2bin_file(data_repository, similarity_model)

        return similarity_model, saved_path_similarity_model


###############################################################################
# Cleaning Model

class Clean:
    def __init__(self):
        pass

    @staticmethod
    def overlap(similarity_model):
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
        old_preprocessed_file_list = Load.binary_file_list(os.path.join(Repository_Path, Preprocessed_Path))
        overlap_preprocessed_file_list = Clean.diff(old_preprocessed_file_list, similarity_model['file_list'])

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
    def diff(list_a, list_b):
        list_b = set(list_b)
        return [item for item in list_a if item not in list_b]


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
                model[row][col] = Model.covariance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def cosine_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = Model.cosine_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def euclidean_distance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = Model.euclidean_distance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def manhattan_distance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = Model.manhattan_distance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = Model.gradient_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def reversed_gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                model[row][col] = Model.reversed_gradient_similarity_score(file_list[row], file_list[col])

        return model
