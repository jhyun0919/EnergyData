# -*- coding: utf-8 -*-

from GlobalParameter import *
import Graph
import Preprocess
import Similarity
import Visualization
import Clustering


def analyze_data(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
    print 'time_interval: ' + str(time_interval) + ' min'
    print 'refined_type: ' + refined_type
    print '--------------------------------------------'

    # Refine the data and save
    refined_data_path = Preprocess.refining_data(time_interval, refined_type)

    # Draw graphs and save the figures
    Graph.Save.figure()

    # Build similarity model and save
    Similarity.Build.similarity_model(time_interval, refined_type)

    # Set data for visualization
    Visualization.set_data4visualization(time_interval, refined_type)

    # Clustering
    Clustering.AffinityProp.build_cluster(time_interval, refined_type, )


if __name__ == '__main__':
    analyze_data(time_interval=1440, refined_type=FullyPreprocessedPath)
