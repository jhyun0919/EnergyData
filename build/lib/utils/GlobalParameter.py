# -*- coding: utf-8 -*-
from datetime import timedelta

# Preprocess
Normalization_Interval = 10  # minute
ts_delta = timedelta(minutes=Normalization_Interval)
Noise_Filter = 10
Scale_Size = 100
Similarity_Matrix_Scaling = 100

# Save
Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository'
Preprocessed_Path = 'preprocessed_data'
Model_Path = 'model'

# Similarity
Round = 3
Gradient_Threshold = 0.5

# Dependency : close
Level = 9
Divider = float(Scale_Size) / Level

# Network
Cosine_Edge_Threshold = 3
Euclidean_Edge_Threshold = 10
Manhattan_Edge_Threshold = 10
Gradient_Edge_Threshold = 11
Reversed_Gradient_Edge_Threshold = 15


# Dependency : far
