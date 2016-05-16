# -*- coding: utf-8 -*-

from GlobalParameter import *
from FileIO import Load
from FileIO import Save
from Preprocess import data_preprocess
import os
from math import sqrt
import numpy as np
from Preprocess import preprocess4similarity


class Similarity():
    def __init__(self):
        pass

    ###############################################################################
    # build similarity model

    @staticmethod
    def build_model(file_list):
        similarity_model = {}

        similarity_model['file_list'] = file_list
        similarity_model['cosine_similarity'] = Similarity.cosine_similarity_model(file_list)
        similarity_model['euclidean_distance'] = Similarity.euclidean_distance_model(file_list)
        similarity_model['gradient_similarity'] = Similarity.gradient_similarity_model(file_list)
        similarity_model['reversed_gradient_similarity'] = Similarity.reversed_gradient_similarity_model(file_list)

        Save.model2bin_file(similarity_model)

        return similarity_model

    @staticmethod
    def cosine_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Similarity.cosine_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def euclidean_distance_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Similarity.euclidean_distance_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Similarity.gradient_similarity_score(file_list[row], file_list[col])

        return model

    @staticmethod
    def reversed_gradient_similarity_model(file_list):
        dimension = len(file_list)
        model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                model[row][col] = Similarity.reversed_gradient_similarity_score(file_list[row], file_list[col])

        return model

    ###############################################################################
    # adding similarity column

    @staticmethod
    def add_similarity_column2model(similarity_model_bin_file, file):
        model = Load.unpickling(similarity_model_bin_file)
        file = Save.preprocessed_data2bin_file(data_preprocess(file))

        # cosine similarity column
        cosine_column = Similarity.cosine_similarity_column(model['file_list'], file)
        cosine_model = np.c_[model['cosine_similarity'], cosine_column]
        cosine_model = np.r_[cosine_model, [np.zeros(len(cosine_model[0]))]]
        model['cosine_similarity'] = cosine_model

        # euclidean distance column
        euclidean_column = Similarity.euclidean_distance_column(model['file_list'], file)
        euclidean_model = np.c_[model['euclidean_distance'], euclidean_column]
        euclidean_model = np.r_[euclidean_model, [np.zeros(len(euclidean_model[0]))]]
        model['euclidean_distance'] = euclidean_model

        # gradient similarity column
        gradient_column = Similarity.gradient_similarity_column(model['file_list'], file)
        gradient_model = np.c_[model['gradient_similarity'], gradient_column]
        gradient_model = np.r_[gradient_model, [np.zeros(len(gradient_model[0]))]]
        model['gradient_similarity'] = gradient_model

        # reversed-gradient similarity column
        reversed_gradient_column = Similarity.reversed_gradient_similarity_column(model['file_list'], file)
        reversed_gradient_model = np.c_[model['reversed_gradient_similarity'], reversed_gradient_column]
        reversed_gradient_model = np.r_[reversed_gradient_model, [np.zeros(len(reversed_gradient_model[0]))]]
        model['reversed_gradient_similarity'] = reversed_gradient_model

        # file list
        model['file_list'].append(file)

        Save.model2bin_file(model)

        return model, file

    ###############################################################################
    # similarity column

    @staticmethod
    def cosine_similarity_column(file_list, file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Similarity.cosine_similarity_score(file_list[row], file)

        return column

    @staticmethod
    def euclidean_distance_column(file_list, file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Similarity.euclidean_distance_score(file_list[row], file)

        return column

    @staticmethod
    def gradient_similarity_column(file_list, file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Similarity.gradient_similarity_score(file_list[row], file)

        return column

    @staticmethod
    def reversed_gradient_similarity_column(file_list, file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Similarity.reversed_gradient_similarity_score(file_list[row], file)

        return column

    ###############################################################################
    # similarity score

    @staticmethod
    def cosine_similarity_score(binary_file_1, binary_file_2):
        early, late, _ = preprocess4similarity(binary_file_1, binary_file_2)
        score = Similarity.cosine_similarity_calculator(early, late)
        return score

    @staticmethod
    def euclidean_distance_score(binary_file_1, binary_file_2):
        early, late, _ = preprocess4similarity(binary_file_1, binary_file_2)
        score = Similarity.euclidean_distance_calculator(early, late)
        return score

    @staticmethod
    def gradient_similarity_score(binary_file_1, binary_file_2):
        early, late, _ = preprocess4similarity(binary_file_1, binary_file_2)
        score = Similarity.gradient_similarity_calculator(early, late)
        return score

    @staticmethod
    def reversed_gradient_similarity_score(binary_file_1, binary_file_2):
        early, late, _ = preprocess4similarity(binary_file_1, binary_file_2)
        score = Similarity.reversed_gradient_similarity_calculator(early, late)
        return score

    ###############################################################################
    # similarity score calculator

    @staticmethod
    def cosine_similarity_calculator(early, late):
        numerator = sum(a * b for a, b in zip(early, late))
        denominator = Similarity.square_rooted(early) * Similarity.square_rooted(late)
        return round(numerator / float(denominator), Round)

    @staticmethod
    def euclidean_distance_calculator(early, late):
        return round(sqrt(sum(pow(a - b, 2) for a, b in zip(early, late))), Round)

    @staticmethod
    def gradient_similarity_calculator(early, late):
        score = []

        early_gradient = np.gradient(early)
        late_gradient = np.gradient(late)

        for a, b, in zip(early_gradient, late_gradient):
            gradient_distance = abs(a - b)
            if gradient_distance < Gradient_Threshold:
                score.append(0)
            else:
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
            if gradient_distance < Gradient_Threshold:
                score.append(0)
            else:
                score.append(gradient_distance)

        return round(sum(score), 3)

    ###############################################################################
    # ordering algorithm

    ###############################################################################
    #

    @staticmethod
    def square_rooted(x):
        return round(sqrt(sum([a * a for a in x])), Round)


if __name__ == '__main__':
    path = os.path.join(Repository_Path, Preprocessed_Path)
    file_list = Load.load_filelist(path)

    # for file in file_list:
    #     print file

    similarity_model = Similarity.build_model(file_list)

    # print similarity_model['euclidean_distance']
    # print similarity_model['cosine_similarity']
    # print similarity_model['gradient_similarity']
    # print similarity_model['reversed_gradient_similarity']

    print similarity_model
