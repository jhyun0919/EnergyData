# -*- coding: utf-8 -*-
from datetime import timedelta

###############################################################################
# Preprocess

Time_Interval = 15  # minute
Noise_Filter = 10
Scale_Size = 100
Similarity_Matrix_Scaling = 100


###############################################################################
# Save

Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository'
Raw_Data_Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository/VTT'
Graph_path = 'graph'
Preprocessed_Path = 'refined_data'
Model_Path = 'model'
Network_Path = 'network_data'


###############################################################################
# Similarity

Round = 3
Gradient_Threshold = 0.5


###############################################################################
# Dependency : close

Level = 9
Divider = float(Scale_Size) / Level


###############################################################################
# Network

Cosine_Edge_Threshold = 3
Euclidean_Edge_Threshold = 10
Manhattan_Edge_Threshold = 10
Gradient_Edge_Threshold = 11
Reversed_Gradient_Edge_Threshold = 15

Deviation_Multiplier = 1
