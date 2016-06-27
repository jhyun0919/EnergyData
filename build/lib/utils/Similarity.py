# -*- coding: utf-8 -*-

from GlobalParameter import *
from FileIO import Load
from FileIO import Save
from Matrix import decalcomanie
from Preprocess import data_preprocess
from math import sqrt
from operator import itemgetter
import numpy as np
from Preprocess import ts_synchronize
from Preprocess import preprocess4similarity_matrix
import os
import networkx as nx
import matplotlib.pyplot as plt
import scipy.stats as stats
import pylab as pl


###############################################################################

class Model:
    def __init__(self):
        pass

    ###############################################################################
    # build similarity model

    @staticmethod
    def build_model(file_list):
        """
        -

        :param file_list:
        :return:
        """
        similarity_model = {}

        similarity_model['file_list'] = file_list
        similarity_model['covariance'] = decalcomanie(Model.covariance_model(file_list))
        similarity_model['cosine_similarity'] = decalcomanie(Model.cosine_similarity_model(file_list))
        similarity_model['euclidean_distance'] = decalcomanie(Model.euclidean_distance_model(file_list))
        similarity_model['manhattan_distance'] = decalcomanie(Model.manhattan_distance_model(file_list))
        similarity_model['gradient_similarity'] = decalcomanie(Model.gradient_similarity_model(file_list))
        similarity_model['reversed_gradient_similarity'] = decalcomanie(
            Model.reversed_gradient_similarity_model(file_list))

        saved_path = Save.model2bin_file(similarity_model)

        return similarity_model, saved_path

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

    ###############################################################################
    # cleaning model

    @staticmethod
    def clean_overlap(similarity_model):
        # clean similarity model
        overlap_list = Model.overlap_detection(similarity_model['file_list'])

        for idx in overlap_list:
            similarity_model['file_list'].pop(idx)
            similarity_model['covariance'] = Model.pop_row_column(similarity_model['covariance'], idx)
            similarity_model['cosine_similarity'] = Model.pop_row_column(similarity_model['cosine_similarity'], idx)
            similarity_model['euclidean_distance'] = Model.pop_row_column(similarity_model['euclidean_distance'], idx)
            similarity_model['manhattan_distance'] = Model.pop_row_column(similarity_model['manhattan_distance'], idx)
            similarity_model['gradient_similarity'] = Model.pop_row_column(similarity_model['gradient_similarity'], idx)
            similarity_model['reversed_gradient_similarity'] = Model.pop_row_column(
                similarity_model['reversed_gradient_similarity'], idx)

        saved_path = Save.model2bin_file(similarity_model)

        # clean preprocessed data repository
        old_preprocessed_file_list = Load.load_binary_file_list(os.path.join(Repository_Path, Preprocessed_Path))
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

        # file list
        model['file_list'].append(data_file)

        # covariance
        covariance_row, covariance_column = Model.covariance_column(model['file_list'], data_file)
        model['covariance'] = np.r_[model['covariance'], covariance_row]
        model['covariance'] = np.c_[model['covariance'], covariance_column]

        # cosine similarity
        cosine_row, cosine_column = Model.cosine_similarity_column(model['file_list'], data_file)
        model['cosine_similarity'] = np.r_[model['cosine_similarity'], cosine_row]
        model['cosine_similarity'] = np.c_[model['cosine_similarity'], cosine_column]

        # euclidean distance
        euclidean_row, euclidean_column = Model.euclidean_distance_column(model['file_list'], data_file)
        model['euclidean_distance'] = np.r_[model['euclidean_distance'], euclidean_row]
        model['euclidean_distance'] = np.c_[model['euclidean_distance'], euclidean_column]

        # manhattan distance
        manhattan_row, manhattan_column = Model.manhattan_distance_column(model['file_list'], data_file)
        model['manhattan_distance'] = np.r_[model['manhattan_distance'], manhattan_row]
        model['manhattan_distance'] = np.c_[model['manhattan_distance'], manhattan_column]

        # gradient similarity
        gradient_row, gradient_column = Model.gradient_similarity_column(model['file_list'], data_file)
        model['gradient_similarity'] = np.r_[model['gradient_similarity'], gradient_row]
        model['gradient_similarity'] = np.c_[model['gradient_similarity'], gradient_column]

        # reversed-gradient similarity
        reversed_gradient_row, reversed_gradient_column = Model.reversed_gradient_similarity_column(model['file_list'],
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
            column[row] = Model.covariance_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def cosine_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.cosine_similarity_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def euclidean_distance_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.euclidean_distance_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def manhattan_distance_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.manhattan_distance_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def gradient_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.gradient_similarity_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    @staticmethod
    def reversed_gradient_similarity_column(file_list, data_file):
        dimension = len(file_list)
        column = np.zeros((dimension, 1))

        for row in xrange(0, dimension):
            column[row] = Model.reversed_gradient_similarity_score(file_list[row], data_file)

        row = np.transpose(column)
        row = row[0][0:-1]
        row = np.reshape(row, (1, len(row)))

        return row, column

    ###############################################################################
    # assign similarity score

    @staticmethod
    def covariance_score(binary_file_1, binary_file_2):
        early, late, _ = ts_synchronize(binary_file_1, binary_file_2)
        score = Model.covariance_calculator(early, late)

        return score

    @staticmethod
    def cosine_similarity_score(binary_file_1, binary_file_2):
        early, late, _ = ts_synchronize(binary_file_1, binary_file_2)
        score = Model.cosine_similarity_calculator(early, late)

        return abs(1 - score)

    @staticmethod
    def euclidean_distance_score(binary_file_1, binary_file_2):
        early, late, _ = ts_synchronize(binary_file_1, binary_file_2)
        score = Model.euclidean_distance_calculator(early, late)

        return score

    @staticmethod
    def manhattan_distance_score(binary_file_1, binary_file_2):
        early, late, length = ts_synchronize(binary_file_1, binary_file_2)
        score = Model.manhattan_distance_calculator(early, late)

        return score / length

    @staticmethod
    def gradient_similarity_score(binary_file_1, binary_file_2):
        early, late, length = ts_synchronize(binary_file_1, binary_file_2)
        score = Model.gradient_similarity_calculator(early, late)

        return score / length

    @staticmethod
    def reversed_gradient_similarity_score(binary_file_1, binary_file_2):
        early, late, length = ts_synchronize(binary_file_1, binary_file_2)
        score = Model.reversed_gradient_similarity_calculator(early, late)

        return score / length

    ###############################################################################
    # calculate similarity score

    @staticmethod
    def covariance_calculator(early, late):
        return np.cov(early, late)[0][1]

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
            score.append(gradient_distance)

        return round(sum(score), 3)

    @staticmethod
    def square_rooted(x):
        return round(sqrt(sum([a * a for a in x])), Round)


###############################################################################

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
        target_column_model['covariance'] = model['covariance'][idx]
        target_column_model['cosine_similarity'] = model['cosine_similarity'][idx]
        target_column_model['euclidean_distance'] = model['euclidean_distance'][idx]
        target_column_model['manhattan_distance'] = model['manhattan_distance'][idx]
        target_column_model['gradient_similarity'] = model['gradient_similarity'][idx]
        target_column_model['reversed_gradient_similarity'] = model['reversed_gradient_similarity'][idx]

        return target_column_model

    @staticmethod
    def sorting_column(target_column_model):
        covariance_sorting_column = Report.sorting_tuples_list(
            Report.binder(target_column_model['covariance'],
                          target_column_model['file_list']))
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

        sorted_column_model['covariance'] = covariance_sorting_column
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
    def sorting_tuples_list(tuples_list, reverse=False):
        tuples_list.sort(key=itemgetter(1), reverse=reverse)

        return tuples_list


###############################################################################

class Network:
    def __init__(self):
        pass

    class Cosine:
        def __init__(self):
            pass

        @staticmethod
        def set_threshold(similarity_model):
            return Network.get_threshold_via_pdf(similarity_matrix=similarity_model['cosine_similarity'])

        @staticmethod
        def build_graph(similarity_model, threshold):
            Network.build_network(similarity_model['file_list'], similarity_model['cosine_similarity'],
                                  threshold, 'cosine_similarity')

    class Euclidean:
        def __init__(self):
            pass

        @staticmethod
        def set_threshold(similarity_model):
            return Network.get_threshold_via_pdf(similarity_matrix=similarity_model['euclidean_distance'])

        @staticmethod
        def build_graph(similarity_model, threshold):
            Network.build_network(similarity_model['file_list'], similarity_model['euclidean_distance'],
                                  threshold, 'euclidean_distance')

    class Manhattan:
        def __init__(self):
            pass

        @staticmethod
        def set_threshold(similarity_model):
            return Network.get_threshold_via_pdf(similarity_matrix=similarity_model['manhattan_distance'])

        @staticmethod
        def build_graph(similarity_model, threshold):
            Network.build_network(similarity_model['file_list'], similarity_model['manhattan_distance'],
                                  threshold, 'manhattan_distance')

    class Gradient:
        def __init__(self):
            pass

        @staticmethod
        def set_threshold(similarity_model):
            return Network.get_threshold_via_pdf(similarity_matrix=similarity_model['gradient_similarity'])

        @staticmethod
        def build_graph(similarity_model, threshold):
            Network.build_network(similarity_model['file_list'], similarity_model['gradient_similarity'],
                                  threshold, 'gradient_similarity')

    class ReversedGradient:
        def __init__(self):
            pass

        @staticmethod
        def set_threshold(similarity_model):
            return Network.get_threshold_via_pdf(similarity_matrix=similarity_model['reversed_gradient_similarity'])

        @staticmethod
        def build_graph(similarity_model, threshold):
            Network.build_network(similarity_model['file_list'], similarity_model['reversed_gradient_similarity'],
                                  threshold, 'reversed_gradient_similarity')

    @staticmethod
    def get_threshold_via_pdf(similarity_matrix):
        scaled_similarity_matrix = preprocess4similarity_matrix(similarity_matrix)
        scaled_similarity_list = []

        for i in xrange(0, len(scaled_similarity_matrix)):
            for j in xrange(0, len(scaled_similarity_matrix)):
                if i != j:
                    scaled_similarity_list.append(scaled_similarity_matrix[i][j])

        scaled_similarity_list.sort()

        pdf_mean = np.mean(scaled_similarity_list)
        pdf_stdev = np.std(scaled_similarity_list)
        pdf = stats.norm.pdf(scaled_similarity_list, pdf_mean, pdf_stdev)
        threshold = pdf_mean - pdf_stdev * Deviation_Multiplier

        print 'similarity matrix: '
        print similarity_matrix
        print
        print 'pdf mean: ' + str(pdf_mean)
        print 'pdf_standard_deviation: ' + str(pdf_stdev)
        print
        print 'threshold = ' + str(threshold)
        print '\t= pdf_mean - pdf_stdev * ' + str(Deviation_Multiplier)

        pl.axvline(threshold, color='r')
        pl.plot(scaled_similarity_list, pdf, '-o')
        pl.hist(scaled_similarity_list, normed=True)
        pl.show()

        return threshold

    @staticmethod
    def build_network(file_path_list, similarity_matrix, threshold, title):
        scaled_similarity_matrix = preprocess4similarity_matrix(similarity_matrix)

        file_list = []

        for line in file_path_list:
            file = line.rsplit('/', 1)[-1]
            file = file.split('.')[0]
            file = file.split('_', 2)[-1]
            file_list.append(file)

        G = nx.MultiDiGraph()

        G.add_nodes_from(file_list)

        for i in xrange(0, len(file_list)):
            for j in xrange(0, len(file_list)):
                if scaled_similarity_matrix[i][j] <= threshold:
                    G.add_edge(file_list[i], file_list[j], weight=scaled_similarity_matrix[i][j])

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos, font_size=9, font_family='sans-serif')
        plt.axis('off')
        plt.title(title)

        plt.show()


###############################################################################


if __name__ == '__main__':
    # path = os.path.join(Repository_Path, Preprocessed_Path)
    # file_list = Load.load_filelist(path)

    # for file in file_list:
    #     print file

    # similarity_model, _ = Model.build_model(file_list)

    # print similarity_model['cosine_similarity']
    # print similarity_model['euclidean_distance']
    # print similarity_model['manhattan_distance']
    # print similarity_model['gradient_similarity']
    # print similarity_model['reversed_gradient_similarity']

    similarity_model = Load.unpickling(
        '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/model/model.bin')

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

    # print similarity_model

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
    # for line in sorted_column_model['manhattan_distance']:
    #     print line
    # print
    # for line in sorted_column_model['gradient_similarity']:
    #     print line
    # print
    # for line in sorted_column_model['reversed_gradient_similarity']:
    #     print line
    # print

    threshold = Network.Cosine.set_threshold(similarity_model)
    Network.Cosine.build_graph(similarity_model, threshold)

    threshold = Network.Euclidean.set_threshold(similarity_model)
    Network.Euclidean.build_graph(similarity_model, threshold)

    threshold = Network.Manhattan.set_threshold(similarity_model)
    Network.Manhattan.build_graph(similarity_model, threshold)

    threshold = Network.Gradient.set_threshold(similarity_model)
    Network.Gradient.build_graph(similarity_model, threshold)

    threshold = Network.ReversedGradient.set_threshold(similarity_model)
    Network.ReversedGradient.build_graph(similarity_model, threshold)

    # print preprocess4similarity_matrix(similarity_model['cosine_similarity'])
    # print preprocess4similarity_matrix(similarity_model['euclidean_distance'])
