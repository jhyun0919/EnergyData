# -*- coding: utf-8 -*-

###############################################################################
# Preprocess

Time_Interval = 60  # minute
Similarity_Matrix_Scaling = 100

###############################################################################
# Save

Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository'

Raw_Data_Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/VTT'

Visualization_Repository = '/Users/JH/Documents/GitHub/EnergyData_jhyun/Visualization'
HeatMap_Path = 'HeatMap'
Network_Path = 'Network'
CalendarHeatMap_Path = 'Calendar_HeatMap'

Graph_path = 'graph'

Fully_Preprocessed_Path = 'refined_data_fully_refined'
Semi_Preprocessed_Path = 'refined_data_skip_interpolation'

Model_Path = 'similarity_model'

###############################################################################
# Similarity

Similarity_Type = ['covariance', 'cosine_similarity', 'euclidean_distance', 'manhattan_distance', 'gradient_similarity',
                   'reversed_gradient_similarity']
Round = 3

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