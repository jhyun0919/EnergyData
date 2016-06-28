# -*- coding: utf-8 -*-

###############################################################################
# Preprocess

Time_Interval = 15  # minute
Similarity_Matrix_Scaling = 100

###############################################################################
# Save

Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository'
Raw_Data_Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/VTT'
Graph_path = 'graph'
Fully_Preprocessed_Path = 'refined_data_fully_refined'
Semi_Preprocessed_Path = 'refined_data_skip_interpolation'
Model_Path = 'similarity_model'
Network_Path = 'network_data'

###############################################################################
# Similarity

Round = 3
Gradient_Threshold = 0.5

###############################################################################
# Network

Cosine_Edge_Threshold = 3
Euclidean_Edge_Threshold = 10
Manhattan_Edge_Threshold = 10
Gradient_Edge_Threshold = 11
Reversed_Gradient_Edge_Threshold = 15

Deviation_Multiplier = 1
