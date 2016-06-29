# -*- coding: utf-8 -*-

from GlobalParameter import *
import Graph
import Preprocess
import Similarity

if __name__ == '__main__':
    # Draw graphs and save the figures
    # graph_directory = Graph.Save.raw_data2graph()

    # Refine the data and save
    fully_refined_directory, skip_interpolation_directory = Preprocess.refining_data()

    # Build similarity model and save
    # Similarity.Build.similarity_model()