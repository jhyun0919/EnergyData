# -*- coding: utf-8 -*-
from datetime import timedelta

# Preprocess
Normalization_Interval = 10  # minute
ts_delta = timedelta(minutes=Normalization_Interval)
Noise_Filter = 10
Scale_Size = 100

# Dependency : close
Level = 9
Divider = float(Scale_Size) / Level
Round = 3

# Dependency : far
Gradient_Threshold = 0.5

# Save
Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository'
Preprocessed_Path = 'preprocessed_data'
Dependency_Path = 'model'
