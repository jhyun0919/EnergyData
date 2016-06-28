# -*- coding: utf-8 -*-

from operator import itemgetter
from FileIO import Load


def similarity_report(file_name):
    pass



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


def sorting_column(target_column_model):
    covariance_sorting_column = sorting_tuples_list(
        binder(target_column_model['covariance'],
               target_column_model['file_list']))
    cosine_sorting_column = sorting_tuples_list(
        binder(target_column_model['cosine_similarity'],
               target_column_model['file_list']))
    euclidean_sorting_column = sorting_tuples_list(
        binder(target_column_model['euclidean_distance'],
               target_column_model['file_list']))
    manhattan_sorting_column = sorting_tuples_list(
        binder(target_column_model['manhattan_distance'],
               target_column_model['file_list']))
    gradient_sorting_column = sorting_tuples_list(
        binder(target_column_model['gradient_similarity'],
               target_column_model['file_list']))
    r_gradient_sorting_column = sorting_tuples_list(
        binder(target_column_model['reversed_gradient_similarity'],
               target_column_model['file_list']))

    sorted_column_model = {}

    sorted_column_model['covariance'] = covariance_sorting_column
    sorted_column_model['cosine_similarity'] = cosine_sorting_column
    sorted_column_model['euclidean_distance'] = euclidean_sorting_column
    sorted_column_model['manhattan_distance'] = manhattan_sorting_column
    sorted_column_model['gradient_similarity'] = gradient_sorting_column
    sorted_column_model['reversed_gradient_similarity'] = r_gradient_sorting_column

    return sorted_column_model


def binder(similarity, file_list):
    tuples_list = []

    for a, b in zip(similarity, file_list):
        item = (b, a)
        tuples_list.append(item)

    return tuples_list


def sorting_tuples_list(tuples_list, reverse=False):
    tuples_list.sort(key=itemgetter(1), reverse=reverse)

    return tuples_list


if __name__ == '__main__':
    pass
