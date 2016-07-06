# -*- coding: utf-8 -*-

###############################################################################
# Preprocess

TimeInterval = 1440  # minute

###############################################################################
# Directory

RepositoryPath = '/Users/JH/Documents/GitHub/EnergyData/repository'

RawDataPath = 'VTT'
UnifyDataLengthPath = 'length_unify'

VisualizationRepository = 'visualization'
HeatMapPath = 'HeatMap'
NetworkPath = 'Network'

GraphPath = 'graph'

FullyPreprocessedPath = 'fully_refined'
SemiPreprocessedPath = 'skip_interpolation_refined'

ModelPath = 'similarity_model'

###############################################################################
# Similarity

SimilarityType = ['covariance', 'cosine_similarity', 'euclidean_distance', 'manhattan_distance', 'gradient_similarity',
                  'reversed_gradient_similarity']
Round = 3

###############################################################################
# Clustering
AffinityPreference = -0.05


"""
###############################################################################
# Network

Cosine_Edge_Threshold = 3
Euclidean_Edge_Threshold = 10
Manhattan_Edge_Threshold = 10
Gradient_Edge_Threshold = 11
Reversed_Gradient_Edge_Threshold = 15

Deviation_Multiplier = 1
"""
