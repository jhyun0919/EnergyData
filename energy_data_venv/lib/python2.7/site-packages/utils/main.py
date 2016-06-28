# -*- coding: utf-8 -*-

from GlobalParameter import *
import Graph
import Preprocess

if __name__ == '__main__':
    Graph.Save.raw_data2graph(Raw_Data_Repository_Path)
    Preprocess.refining_data(raw_data_repository_path=Raw_Data_Repository_Path, time_interval=Time_Interval)
