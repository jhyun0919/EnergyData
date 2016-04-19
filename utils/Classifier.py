# -*- coding: utf-8 -*-

import numpy as np
from sklearn.naive_bayes import GaussianNB


# cluster_structure를 입력받아
# classifier를 구성 & 학습시켜
# 반환
def train_clf(cluster_structure):
    X = np.array(cluster_structure['vec_data'])
    Y = np.array(cluster_structure['cluster_tag'])

    clf = GaussianNB()
    # clf = BernoulliNB()
    # clf = MultinomialNB()
    clf.fit(X, Y)

    return clf
