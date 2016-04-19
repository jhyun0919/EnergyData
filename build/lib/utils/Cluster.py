# -*- coding: utf-8 -*-

from sklearn.cluster import AffinityPropagation
from GlobalParam import *


# def __init__(self, AF_PREFERENCE):
#     self.AF_PREFERENCE = AF_PREFERENCE


# vector_dictionary를 입력받아
# AffinityPropagation clustering을 통해
# 각각의 vector들에 적합한 cluster를 구성한 뒤,
# list형식의 cluster를 반환
def affinity_propagation(vector_dic):
    vectors = vector_dic['vec_data']

    return AffinityPropagation(preference=AF_PREFERENCE).fit_predict(vectors)


# vector_dictionary와 cluster를 입력받아
# cluster_structure를 구성하여
# dictionary 형식으로 반환
def make_cluster_structure(vector_dic, clusters):
    cluster_structure = {}

    cluster_structure['file_name'] = vector_dic['file_name']
    cluster_structure['vec_data'] = vector_dic['vec_data']
    cluster_structure['cluster_tag'] = clusters

    return cluster_structure
