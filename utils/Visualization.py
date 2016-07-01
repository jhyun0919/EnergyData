# -*- coding: utf-8 -*-
from FileIO import Load
from FileIO import Save
import cPickle as pickle
import os
from GlobalParameter import *
from operator import itemgetter


def set_data4visualization(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
    print 'setting data for visualization'
    HeatMap.set_data(time_interval, refined_type)
    CalendarHeatMap.set_data()
    Network.set_data()


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
        print '\t',
        print 'HeatMap [O]'

        # set tsv file name
        tsv_file_path = os.path.join(RepositoryPath, VisualizationRepository, HeatMapPath)
        Save.assure_path_exist(tsv_file_path)
        tsv_file_name = 'sensor_data.tsv'
        tsv_file_name = os.path.join(tsv_file_path, tsv_file_name)

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
                        str(i + 1) + "\t" + str(col_idx) + "\t" + str(refined_data['value'][i] * 10) + "\n")

        # write label data
        HeatMap.set_row_label(time_interval, refined_type)
        HeatMap.set_col_label(time_interval, refined_type)

        # write cluster report data
        HeatMap.set_cluster_report(time_interval, refined_type)

    @staticmethod
    def set_row_label(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
        # set tsv file name
        tsv_file_name = 'RowLabel.tsv'
        tsv_file_name = os.path.join(RepositoryPath, VisualizationRepository, HeatMapPath, tsv_file_name)

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
        tsv_file_name = os.path.join(RepositoryPath, VisualizationRepository, HeatMapPath, tsv_file_name)

        # write tsv file with data
        with open(tsv_file_name, "w") as record_file:
            file_list = Load.binary_file_list(os.path.join(RepositoryPath, str(time_interval), refined_type))
            for line in file_list:
                record_file.write('\'' + line.rsplit('/', 1)[-1] + '\'' + '\n')

    @staticmethod
    def set_cluster_report(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
        # load similarity model
        similarity_model_path = os.path.join(RepositoryPath, str(time_interval), refined_type,
                                             ModelPath, 'similarity.bin')
        similarity_model = pickle.load(open(similarity_model_path))

        # write a cluster report for each similarity model type
        for similarity_type in SimilarityType:
            # set tsv file name
            tsv_file_name = similarity_type + '.tsv'
            tsv_file_name = os.path.join(RepositoryPath, VisualizationRepository, HeatMapPath, tsv_file_name)

            # write tsv file with data
            with open(tsv_file_name, "w") as record_file:
                report = HeatMap.Report.sorting_foo(similarity_model[similarity_type][0], similarity_model['file_list'])
                record_file.write(str(report))

    class Report:
        def __init__(self):
            pass

        ###############################################################################
        # ordering algorithm

        @staticmethod
        def sorting_foo(similarity_model, file_list):
            report = []

            tuple_list = HeatMap.Report.binder(similarity_model, file_list)
            tuple_list.sort(key=itemgetter(1), reverse=False)

            for line in file_list:
                for sort_idx in xrange(len(tuple_list)):
                    if line == tuple_list[sort_idx][0]:
                        report.append(sort_idx + 1)

            return report

        @staticmethod
        def binder(similarity, file_list):
            tuples_list = []

            for a, b in zip(similarity, file_list):
                item = (b, a)
                tuples_list.append(item)

            return tuples_list


class CalendarHeatMap:
    def __init__(self):
        pass

    @staticmethod
    def set_data():
        print '\t',
        print 'Calendar_HeatMap [X]'


class Network:
    def __init__(self):
        pass

    @staticmethod
    def set_data():
        print '\t',
        print 'Network [X]'


if __name__ == '__main__':
    HeatMap.set_data()
