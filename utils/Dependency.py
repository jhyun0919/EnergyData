# -*- coding: utf-8 -*-

from GlobalParameter import *
from Preprocess import preprocess4dependcy
import Graph
import matplotlib.pyplot as plt
import numpy as np
from Load import load_filelist


def close_dependency_score(binary_file_1, binary_file_2):
    early, late, length = preprocess4dependcy(binary_file_1, binary_file_2)

    close_score = close_score_calculator(early, late, length)

    return close_score


def close_score_calculator(early, late, length):
    similarity = []

    for i in xrange(0, length):
        early_data = int(early['value'][i] / Divider)
        late_data = int(late['value'][i] / Divider)

        if early_data == late_data:
            similarity.append(1)
        else:
            similarity.append(0)

    # x = np.linspace(0, length, length)
    # plt.scatter(x, similarity)
    # plt.show()
    # plt.close()

    counter = 0
    for i in similarity:
        if i == 1:
            counter += 1
    similarity_rate = float(counter) / length

    return similarity_rate


def far_dependency_score(binary_file_1, binary_file_2):
    early, late, length = preprocess4dependcy(binary_file_1, binary_file_2)

    far_score = far_score_calculator(early, late, length)

    return far_score


def far_score_calculator(early, late, length):
    dissimilarity = 0

    early_gradient = np.gradient(early['value'])
    late_gradient = np.gradient(late['value'])

    for i in xrange(0, length):
        distance = abs(early_gradient[i] - late_gradient[i])

        if early_gradient[i] * late_gradient[i] < 0:
            dissimilarity += distance
        elif distance > Gradient_Threshold:
            dissimilarity += distance

    return dissimilarity


def close_dependency_model(file_list):
    dimension = len(file_list)
    model = np.zeros((dimension, dimension))

    for row in xrange(0, dimension):
        for col in xrange(row + 1, dimension):
            score = close_dependency_score(file_list[row], file_list[col])
            model[row][col] = score

    return model


def far_dependency_model(file_list):
    dimension = len(file_list)
    model = np.zeros((dimension, dimension))

    for row in xrange(0, dimension):
        for col in xrange(row + 1, dimension):
            score = far_dependency_score(file_list[row], file_list[col])
            model[row][col] = score

    return model


def dependency_model(close_model, far_model):
    dimension = len(close_model[0])
    model = np.zeros((dimension, dimension))

    for row in xrange(0, dimension):
        for col in xrange(row + 1, dimension):
            score = far_model[row][col] / close_model[row][col]
            model[row][col] = int(score)

    return model


if __name__ == '__main__':
    path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/utils/VTT'

    file_list = load_filelist(path)

    for file in file_list:
        print file

    # data_dictionary_1 = unpickling(file_path_1)
    # data_dictionary_2 = unpickling(file_path_2)
    # data_dictionary_3 = unpickling(file_path_3)
    # Graph.Show.dic2graph(data_dictionary_1)
    # Graph.Show.dic2graph(data_dictionary_2)
    # Graph.Show.dic2graph(data_dictionary_3)

    close_model = close_dependency_model(file_list)
    print close_model

    far_model = far_dependency_model(file_list)
    print far_model

    model = dependency_model(close_model, far_model)
    print model

