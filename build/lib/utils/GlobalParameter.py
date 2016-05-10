# -*- coding: utf-8 -*-
from datetime import timedelta

# Preprocess
Interpolation_Interval = 10  # minute
ts_delta = timedelta(minutes=Interpolation_Interval)
Noise_Filter = 10
Scale_Size = 100

# Dependency : close
Level = 9
Divider = float(Scale_Size) / Level

# Dependency : far
Gradient_Threshold = 0.5

# Save
Repository_Path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/repository'

