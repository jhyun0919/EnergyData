# -*- coding: utf-8 -*-

from FileIO import Load
from dtw import dtw
import os
from GlobalParameter import *
import cPickle as pickle
import numpy as np
from Matrix import symmetric
from numpy.linalg import norm


class Self:
    def __init__(self):
        pass

    @staticmethod
    def set_time_slot(time_slot=Month, time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
        print 'set time slot: '
        file_list = Load.binary_file_list(os.path.join(RepositoryPath, str(time_interval), refined_type))

        if time_slot == 'month':
            for line in file_list:
                Self.set_cluster(Self.set_dissimilarity_matrix(Self.monthly_slot(line)))

        elif time_slot == 'week':
            for line in file_list:
                Self.set_cluster(Self.set_dissimilarity_matrix(Self.weekly_slot(line)))
        if time_slot == 'day':
            for line in file_list:
                Self.daily_slot(line)

    @staticmethod
    def monthly_slot(binary_data_path):
        print 'monthly: ',
        print binary_data_path.rsplit('/', 1)[-1]
        value_in_slot = []
        data = pickle.load(open(binary_data_path))

        temp_idx = 0
        for idx in xrange(0, len(data['ts'])):
            if idx == len(data['ts']) - 1:
                # print data['ts'][idx]
                value_in_slot.append(data['value'][temp_idx:])
            elif data['ts'][idx].month != data['ts'][idx + 1].month:
                # print data['ts'][idx]
                value_in_slot.append(data['value'][temp_idx:idx + 1])
                temp_idx = idx + 1

        # 처음과 마지막은 완전한 slot 을 못이룰 수 있는 가능성이 있음
        # slicing 으로 삭제
        return np.asanyarray(value_in_slot[1:-1])

    @staticmethod
    def weekly_slot(binary_data_path):
        print 'weekly: ',
        print binary_data_path.rsplit('/', 1)[-1]
        value_in_slot = []
        data = pickle.load(open(binary_data_path))

        temp_idx = 0
        for idx in xrange(0, len(data['ts'])):
            if data['ts'][idx].weekday() == 6:
                # print data['ts'][idx].weekday()
                value_in_slot.append(data['value'][temp_idx:idx + 1])
                temp_idx = idx + 1

        # 처음과 마지막은 완전한 slot 을 못이룰 수 있는 가능성이 있음
        # slicing 으로 삭제
        return np.asanyarray(value_in_slot[1:-1])

    @staticmethod
    def daily_slot(binary_data_path):
        print 'daily: ',
        print binary_data_path.rsplit('/', 1)[-1]
        value_in_slot = []
        data = pickle.load(open(binary_data_path))

        temp_idx = 0
        for idx in xrange(0, len(data['ts'])):
            if idx == len(data['ts']) - 1:
                # print data['ts'][idx]
                value_in_slot.append(data['value'][temp_idx:])
            elif data['ts'][idx].day != data['ts'][idx + 1].day:
                # print data['ts'][idx]
                value_in_slot.append(data['value'][temp_idx:idx + 1])
                temp_idx = idx + 1

        # 처음과 마지막은 완전한 slot 을 못이룰 수 있는 가능성이 있음
        # slicing 으로 삭제
        return np.asanyarray(value_in_slot[1:-1])

    @staticmethod
    def set_dissimilarity_matrix(slot_array):
        dimension = len(slot_array)
        dissimilarity_model = np.zeros((dimension, dimension))

        for row in xrange(0, dimension):
            for col in xrange(row, dimension):
                dissimilarity_model[row][col] = dtw(slot_array[row], slot_array[col], dist=norm)

        print dissimilarity_model

        return symmetric(dissimilarity_model)

    @staticmethod
    def set_cluster(dissimilarity_model):
        pass

    @staticmethod
    def set_population_vector():
        pass

    @staticmethod
    def set_euclidean_vector():
        pass

    @staticmethod
    def get_anomaly_score():
        pass

    @staticmethod
    def show_anomaly_score():
        pass


class Neighbor:
    def __init__(self):
        pass

    @staticmethod
    def get_cluster_info():
        pass

    @staticmethod
    def set_dissimilarity_matrix():
        pass

    @staticmethod
    def get_anomaly_score():
        pass

    @staticmethod
    def show_anomaly_score():
        pass


###############################################################################


if __name__ == '__main__':
    Self.set_time_slot(Week)
