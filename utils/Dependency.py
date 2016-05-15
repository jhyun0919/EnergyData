# -*- coding: utf-8 -*-

from GlobalParameter import *
from Preprocess import preprocess4dependcy
from Preprocess import data_preprocess
import os
import Graph
import matplotlib.pyplot as plt
import numpy as np
import FileIO
from collections import OrderedDict
from Matrix import decalcomanie


def close_dependency_score(binary_file_1, binary_file_2):
    """
    - 두 file 사이 close dependency를 구하기 위해 전처리 수행
    - 전처리 된 두 data 사이 close dependency를 계산

    :param binary_file_1:
    :param binary_file_2:
    :return:
    """
    early, late, length = preprocess4dependcy(binary_file_1, binary_file_2)

    close_score = close_score_calculator(early, late, length)

    return close_score


def close_score_calculator(early, late, length):
    """
    - 두 data 사이 close dependency를 계산

    :param early:
    :param late:
    :param length:
    :return:
    """
    similarity = []

    for i in xrange(0, length):
        early_data = int(early['value'][i] / Divider)
        late_data = int(late['value'][i] / Divider)

        # if early_data == late_data:
        #     similarity.append(1)
        # else:
        #     similarity.append(0)

        if early_data == late_data:
            similarity.append(0)
        else:
            similarity.append(abs(early_data - late_data))

    similarity_rate = float(similarity.count(1)) / length

    return similarity_rate


def far_dependency_score(binary_file_1, binary_file_2):
    """
    - 두 file 사이 far dependency를 구하기 위해 전처리 수행
    - 전처리 된 두 data 사이 far dependency를 계산

    :param binary_file_1:
    :param binary_file_2:
    :return:
    """
    early, late, length = preprocess4dependcy(binary_file_1, binary_file_2)

    far_score = far_score_calculator(early, late, length)

    return far_score


def far_score_calculator(early, late, length):
    """
    - 두 data 사이 close dependency를 계산

    :param early:
    :param late:
    :param length:
    :return:
    """
    dissimilarity = []

    early_gradient = np.gradient(early['value'])
    late_gradient = np.gradient(late['value'])

    for i in xrange(0, length):
        distance = abs(early_gradient[i] - late_gradient[i])

        if early_gradient[i] * late_gradient[i] < 0:
            dissimilarity.append(distance)
        elif distance > Gradient_Threshold:
            dissimilarity.append(distance)
        else:
            dissimilarity.append(0)

    return sum(dissimilarity)


def close_dependency_model(file_list):
    """
    - file_list의 file들 사이 close dependency model를 구하는 함수

    :param file_list:
    :return:
    """
    dimension = len(file_list)
    model = np.zeros((dimension, dimension))

    for row in xrange(0, dimension):
        for col in xrange(row + 1, dimension):
            score = close_dependency_score(file_list[row], file_list[col])
            try:
                model[row][col] = 1 / score
            except ZeroDivisionError as err:
                print err
                # =================
                # 다시 생각해 볼 부분
                # =================
                model[row][col] = -1
                # ==================

    return model


def close_dependency_col(file_list, file):
    dimension = len(file_list)
    model = np.zeros((dimension, 1))

    for row in xrange(0, dimension):
        score = close_dependency_score(file_list[row], file)
        try:
            model[row] = 1 / score
        except ZeroDivisionError as err:
            print err
            # =================
            # 다시 생각해 볼 부분
            # =================
            model[row] = -1
            # ==================

    return model


def far_dependency_model(file_list):
    """
    - file_list의 file들 사이 far dependency model를 구하는 함수

    :param file_list:
    :return:
    """
    dimension = len(file_list)
    model = np.zeros((dimension, dimension))

    for row in xrange(0, dimension):
        for col in xrange(row + 1, dimension):
            score = far_dependency_score(file_list[row], file_list[col])
            model[row][col] = score

    return model


def far_dependency_col(file_list, file):
    dimension = len(file_list)
    model = np.zeros((dimension, 1))

    for row in xrange(0, dimension):
        score = far_dependency_score(file_list[row], file)
        model[row] = score

    return model


def dependency_model(file_list):
    """
    - file_list의 file들 사이 dependency model를 구하는 함수
    - close, far, total dependency를 계산

    :param file_list:
        file들의 abs_path를 저장하는 parameter
         -type: list
    :return:
        dependency_model
        -dictionary{"file_list": [], "close_model": np.array[], "far_model": np.array[], "dependency_model": np.array[]}
    """
    model_structure = {}

    close_model = close_dependency_model(file_list)
    far_model = far_dependency_model(file_list)

    model = decalcomanie(close_model * far_model)

    model_structure['file_list'] = file_list
    model_structure['close_model'] = close_model
    model_structure['far_model'] = far_model
    model_structure['dependency_model'] = model

    return model_structure


def append_dependency_model(model_structure_binary_file, file):
    """

    :param model_structure_binary_file:
    :param file:
    :return:
    """
    model_structure = FileIO.Load.unpickling(model_structure_binary_file)
    # 해당 file을 preprocessing 한 뒤 저장
    # 저장된 data를 load 하여 사용
    file = FileIO.Save.preprocessed_data2bin_file(data_preprocess(file))

    close_col = close_dependency_col(model_structure['file_list'], file)
    close_model = np.c_[model_structure['close_model'], close_col]
    close_model = np.r_[close_model, [np.zeros(len(close_model[0]))]]
    model_structure['close_model'] = close_model

    far_col = far_dependency_col(model_structure['file_list'], file)
    far_model = np.c_[model_structure['far_model'], far_col]
    far_model = np.r_[far_model, [np.zeros(len(far_model[0]))]]
    model_structure['far_model'] = far_model

    model_structure['dependency_model'] = decalcomanie(close_model * far_model)

    model_structure['file_list'].append(file)

    FileIO.Save.dependency_model2bin_file(model_structure)

    return model_structure, file


def dependency_ordering(model_structure_binary_file, binary_file_name):
    """

    :param model_structure_binary_file:
    :param binary_file_name:
    :return:
    """
    target_dictionary = find_ordering_target(model_structure_binary_file, binary_file_name)
    target_dictionary = OrderedDict(sorted(target_dictionary.items()))
    target_list = dictionary2list(target_dictionary)

    return target_list


def find_ordering_target(model_structure_binary_file, binary_file_name):
    """

    :param model_structure_binary_file:
    :param binary_file_name:
    :return:
    """
    # try:
    #     file_abs_path = os.path.abspath(binary_file_name)
    # except IOError as err:
    #     print err

    model_structure = FileIO.Load.unpickling(model_structure_binary_file)

    for i in xrange(0, len(model_structure['file_list'])):
        # ===================
        # 수정이 필요한 부분
        # ===================
        if model_structure['file_list'][i] == binary_file_name:
            idx = i
            break
        if i == (len(model_structure['file_list']) - 1):
            print 'There is no target_info in dependency_model.bin'
            exit()

    target_dictionary = {}

    for i in xrange(0, len(model_structure['file_list'])):
        target_dictionary[model_structure['dependency_model'][idx][i]] = model_structure['file_list'][i]

    return target_dictionary


def target_list2file_list(target_list):
    """

    :param target_list:
    :return:
    """
    file_list = []
    for line in target_list:
        file_list.append(line[0])

    return file_list


def dictionary2list(dictionary):
    """

    :param dictionary:
    :return:
    """
    list = []

    for dependency, file_name in dictionary.iteritems():
        temp_list = []
        temp_list.append(file_name)
        temp_list.append(dependency)

        list.append(temp_list)

    return list


if __name__ == '__main__':
    # path = os.path.join(Repository_Path, Preprocessed_Path)
    #
    # file_list = FileIO.Load.load_filelist(path)
    #
    # model_structure = dependency_model(file_list)
    # print model_structure

    # FileIO.Save.dependency_model2bin_file(model_structure)
    #
    # model = FileIO.Load.unpickling(
    #     '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/dependency_model/dependency_model.bin')
    # # print model
    #
    # model = append_dependency_model(
    #     '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/dependency_model/dependency_model.bin',
    #     '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/preprocessed_data/VTT_GW1_HA10_VM_EP_KV_K.bin')
    # print model

    target = dependency_ordering(
        '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/dependency_model/dependency_model.bin',
        '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/preprocessed_data/PP_VTT_GW2_HA7_VM_EP_KV_K.bin')
    print target
