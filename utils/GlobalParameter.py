# -*- coding: utf-8 -*-

###############################################################################
# Preprocess

TimeInterval = 15  # minute

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

###############################################################################
# Abnormal Detection

Month = 'month'
Week = 'week'
Day = 'day'
