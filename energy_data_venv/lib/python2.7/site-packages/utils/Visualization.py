# -*- coding: utf-8 -*-
from FileIO import Load
import cPickle as pickle
import os
from GlobalParameter import *
from operator import itemgetter


class HeatMap:
    def __init__(self):
        pass

    @staticmethod
    def set_data(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
        """
        - HeatMap 에 필요한 data 를 time-interval 과 refined-type 에 맟주어 tsv 형식으로 가공하여 저장

        :param time_interval:
            time interval
        :param refined_type:
            refined type
        :return:
            NA
        """
        # set tsv file name
        tsv_file_name = 'sensor_data.tsv'
        tsv_file_name = os.path.join(VisualizationRepository, HeatMapPath, tsv_file_name)

        # write tsv file with data
        with open(tsv_file_name, "w") as record_file:
            record_file.write("row_idx  col_idx log2ratio\n")

            col_idx = 0
            for refined_binary_file in Load.binary_file_list(
                    os.path.join(RepositoryPath, str(time_interval), refined_type)):

                # unpickling data
                refined_data = pickle.load(open(refined_binary_file))

                # set col_idx
                col_idx += 1
                for i in xrange(0, len(refined_data['value'])):
                    record_file.write(
                        str(i + 1) + "\t" + str(col_idx) + "\t" + str(refined_data['value'][i]) + "\n")

        # write label data
        HeatMap.set_row_label(time_interval, refined_type)
        HeatMap.set_col_label(time_interval, refined_type)

        # write cluster report data
        # HeatMap.set_cluster_report(time_interval, refined_type)

    @staticmethod
    def set_row_label(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
        # set tsv file name
        tsv_file_name = 'RowLabel.tsv'
        tsv_file_name = os.path.join(VisualizationRepository, HeatMapPath, tsv_file_name)

        # write tsv file with data
        with open(tsv_file_name, "w") as record_file:
            file_list = Load.binary_file_list(os.path.join(RepositoryPath, str(time_interval), refined_type))
            refined_data = pickle.load(open(file_list[0]))
            for line in refined_data['ts']:
                record_file.write('\'' + str(line) + '\'' + '\n')

    @staticmethod
    def set_col_label(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
        # set tsv file name
        tsv_file_name = 'ColLabel.tsv'
        tsv_file_name = os.path.join(VisualizationRepository, HeatMapPath, tsv_file_name)

        # write tsv file with data
        with open(tsv_file_name, "w") as record_file:
            file_list = Load.binary_file_list(os.path.join(RepositoryPath, str(time_interval), refined_type))
            for line in file_list:
                record_file.write('\'' + line.rsplit('/', 1)[-1] + '\'' + '\n')

    @staticmethod
    def set_cluster_report(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
        # load similarity model
        similarity_model = pickle.load(
            Load.binary_file_list(os.path.join(RepositoryPath, str(time_interval), refined_type, ModelPath)))

        for similarity_type in SimilarityType:
            # set tsv file name
            tsv_file_name = similarity_type + 'tsv'
            tsv_file_name = os.path.join(VisualizationRepository, HeatMapPath, tsv_file_name)

            # write tsv file with data
            with open(tsv_file_name, "w") as record_file:
                pass

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
            covariance_sorting_column = HeatMap.Report.sorting_tuples_list(
                HeatMap.Report.binder(target_column_model['covariance'],
                                      target_column_model['file_list']))
            cosine_sorting_column = HeatMap.Report.sorting_tuples_list(
                HeatMap.Report.binder(target_column_model['cosine_similarity'],
                                      target_column_model['file_list']))
            euclidean_sorting_column = HeatMap.Report.sorting_tuples_list(
                HeatMap.Report.binder(target_column_model['euclidean_distance'],
                                      target_column_model['file_list']))
            manhattan_sorting_column = HeatMap.Report.sorting_tuples_list(
                HeatMap.Report.binder(target_column_model['manhattan_distance'],
                                      target_column_model['file_list']))
            gradient_sorting_column = HeatMap.Report.sorting_tuples_list(
                HeatMap.Report.binder(target_column_model['gradient_similarity'],
                                      target_column_model['file_list']))
            r_gradient_sorting_column = HeatMap.Report.sorting_tuples_list(
                HeatMap.Report.binder(target_column_model['reversed_gradient_similarity'],
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


class CalendarHeatMap:
    def __init__(self):
        pass

    @staticmethod
    def write_data():
        pass


class Network:
    def __init__(self):
        pass

    @staticmethod
    def write_data():
        pass


if __name__ == '__main__':
    HeatMap.set_data()
