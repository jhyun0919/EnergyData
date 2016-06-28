# -*- coding: utf-8 -*-

from GlobalParameter import *
import Graph
import Preprocess

if __name__ == '__main__':
    # Draw graphs and save the figures
    graph_directory = Graph.Save.raw_data2graph(Raw_Data_Repository_Path)

    # Refine the data and save
    fully_refined_directory, skip_interpolation_directory = Preprocess.refining_data(
        raw_data_repository_path=Raw_Data_Repository_Path, time_interval=Time_Interval)

    # Build similarity model and save
