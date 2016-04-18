# -*- coding: utf-8 -*-

import os
import sys
import cPickle as pickle
import numpy as np
import copy
import time
import matplotlib.pyplot as plt
from sklearn.cluster import AffinityPropagation
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import NearestNeighbors


class LoadData:
    def __init__(self):
        pass

    # 외부에서 argv[ ]로 전달된 directory를
    # 반환
    @staticmethod
    def get_directory():
        try:
            dir_name = sys.argv[1]
            return dir_name
        except IndexError as err:
            print('IndexError: ' + str(err))
            print('Put a directory path as an input argument')
            exit()

    # directory를 입력받아
    # 그 디렉토리 내 binary file들의 절대경로를
    # list로 만들어 반환
    @staticmethod
    def load_file(dir_name):
        bin_file_list = []

        try:
            file_names = os.listdir(dir_name)
            abs_dir = os.path.dirname(os.path.abspath(__file__))

            for file_name in file_names:
                full_filename = os.path.join(dir_name, file_name)
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.bin':
                    file = os.path.join(abs_dir, dir_name, file_name)
                    bin_file_list.append(file)
        except OSError as err:
            print 'OSError' + str(err)

        return bin_file_list

    # binary file을 unpickling 처리하여
    # 읽어옴
    @staticmethod
    def unpickling(bin_file):
        data = pickle.load(open(bin_file))
        return data


class SaveData:
    def __init__(self, RESULT_DIRECTORY, VEC_DIMENSION=None, CLUSTER_STRUCTURE_NAME=None):
        self.RESULT_DIRECTORY = RESULT_DIRECTORY

        if VEC_DIMENSION is not None:
            self.VEC_DIMENSION = VEC_DIMENSION

        if CLUSTER_STRUCTURE_NAME is not None:
            self.CLUSTER_STRUCTURE_NAME = CLUSTER_STRUCTURE_NAME

    # vector_dictionary를
    # binary_file로 바꾸어
    # RESULT_DICETORY에 저장
    def dictionary2bin(self, vec_dic):
        old_path = os.getcwd()

        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        bin_name = sys.argv[1] + '_' + str(self.VEC_DIMENSION) + '_vec.bin'

        f = open(bin_name, 'wb')
        pickle.dump(vec_dic, f, 1)
        f.close()

        os.chdir(old_path)

    # vector_dictionary를
    # text_file로 바꾸어
    # RESULT_DICETORY에 저장
    def dictionary2txt(self, vec_dic):
        old_path = os.getcwd()

        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        txt_name = sys.argv[1] + '_' + str(self.VEC_DIMENSION) + '_vec.txt'

        f = open(txt_name, 'w')
        for line in vec_dic:
            f.write(line + '\n')
            for i in xrange(len(vec_dic[line])):
                f.write(str(vec_dic[line][i]) + '\n')
        f.close()

        os.chdir(old_path)

    # bin_file list를 전달받아
    # 각각의 bin_file을 그래프로 그려
    # RESULT_DIRECTORY에 저장함
    def bins2graphs(self, file_list):
        old_path = os.getcwd()

        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY, 'graph')
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        for file in file_list:
            print 'vector2graph ' + file,
            start_time = time.time()

            x = []
            for line in LoadData.unpickling(file)['ts']:
                x.append(line[0])
            y = LoadData.unpickling(file)['value']

            plt.scatter(x, y, marker='x')

            file_name = file.rsplit('/', 1)[1]

            file_name = file_name.split('.')[0] + '.jpg'

            plt.savefig(file_name)
            plt.close()

            end_time = time.time()
            print '\t\t' + 'run time: ' + str(end_time - start_time)

        os.chdir(old_path)

    # bin_file을 전달받아
    # 그래프로 그려
    # 현재의 경로에 저장힘
    def bin2graph(self, file):
        start_time = time.time()
        print 'vector 2 graph ' + file,

        x = []
        for line in LoadData.unpickling(file)['ts']:
            x.append(line[0])
        y = LoadData.unpickling(file)['value']

        plt.scatter(x, y, marker='x')

        file_name = file.rsplit('/', 1)[-1]

        file_name = file_name.split('.')[0] + '.jpg'

        plt.savefig(file_name)
        plt.close()

        end_time = time.time()

        print '\t\t' + 'run time: ' + str(end_time - start_time)

    # vector dictionary를 전달받아
    # 각각의 vector를 그래프로 그려
    # RESULT_DIRECTORY에 저장함
    def vectors2graphs(self, vectors):
        old_path = os.getcwd()

        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY, 'graph', 'vectorize', str(self.VEC_DIMENSION))
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        for i in xrange(len(vectors['file_name'])):
            start_time = time.time()

            name = vectors['file_name'][i].rsplit('/', 1)[1]

            print 'drawing graph of VECTORIZED ' + name,

            name = name.split('.')[0]
            name = name + '_vec_' + str(self.VEC_DIMENSION) + '.jpg'

            x = np.linspace(0, 1, len(vectors['vec_data'][i]))
            plt.scatter(x, vectors['vec_data'][i], marker='+')
            plt.savefig(name)
            plt.close()

            end_time = time.time()

            print '\t\t' + 'run time: ' + str(end_time - start_time)

        os.chdir(old_path)

    # bin_file의 이름 list인 names와
    # clusters를 전달받아
    # 각각의 bin_file을 그래프로 그려
    # cluster에 따라 분류하여
    # RESULT_DIRECTORY에 저장함
    def clusters2graph(self, cluster_structure):
        old_path = os.getcwd()

        # names = cluster_structure['file_name']
        # clusters = cluster_structure['cluster_tag']

        # 출력 디렉토리로 이동
        # path_old = os.getcwd()
        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY, 'clustered_graph', str(self.VEC_DIMENSION))
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        # 출력 디렉토리 내에서
        # 그래프를 그려 각각 clusters에 해당하는 폴더에 분류하여 저잫함
        for i in xrange(0, len(cluster_structure['file_name'])):
            path_temp = os.path.join(path, str(cluster_structure['cluster_tag'][i]))
            if not os.path.exists(path_temp):
                os.makedirs(path_temp)
            os.chdir(path_temp)
            self.bin2graph(cluster_structure['file_name'][i])
            os.chdir(path)

        os.chdir(old_path)

    # cluster_structure를 입력받아
    # binary file로 변환 후
    # RESULT_DIRECTORY에 저장함
    def cluster_structure2bin(self, cluster_structure):
        old_path = os.getcwd()

        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        bin_name = self.CLUSTER_STRUCTURE_NAME + '_' + str(self.VEC_DIMENSION) + '_vec.bin'
        f = open(bin_name, 'wb')
        pickle.dump(cluster_structure, f, 1)
        f.close()

        os.chdir(old_path)


    # dependency를
    # binary_file로 바꾸어
    # RESULT_DICETORY에 저장
    def dependency2bin(self, dependency_dic):
        old_path = os.getcwd()

        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        bin_name = 'dependency.bin'

        f = open(bin_name, 'wb')
        pickle.dump(dependency_dic, f, 1)
        f.close()

        os.chdir(old_path)

    # dependency를
    # text_file로 바꾸어
    # RESULT_DICETORY에 저장
    def dependency2txt(self, dependency_dic):
        old_path = os.getcwd()

        path = os.path.join(os.getcwd(), self.RESULT_DIRECTORY)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        txt_name = 'dependency.txt'

        f = open(txt_name, 'w')
        for line in dependency_dic:
            f.write(line + '\n')
            for i in xrange(len(dependency_dic[line])):
                f.write(str(dependency_dic[line][i]) + '\n')
        f.close()

        os.chdir(old_path)


class Data2Vec:
    def __init__(self, VEC_DIMENSION, INTERPOLATION_INTERVAL, SCALE_SIZE):
        self.VEC_DIMENSION = VEC_DIMENSION
        self.INTERPOLATION_INTERVAL = INTERPOLATION_INTERVAL
        self.SCALE_SIZE = SCALE_SIZE

    # binnary_file list를 입력 받아
    # 각각의 binary_file을 vector로 전처리한 뒤,
    # dictionary로 구성하여 반환
    def bins2vectors2dic(self, file_list):
        vector_dic = {}

        vector_dic['file_name'] = np.asarray(file_list)
        data = []

        for file in vector_dic['file_name']:
            try:
                print 'data2vector ' + file,
                start_time = time.time()
                data.append(self.trim_data(file))
            except:
                print 'An error occurred'
            finally:
                end_time = time.time()
                print '\t\t' + 'run time: ' + str(end_time - start_time)

        vector_dic['vec_data'] = np.asarray(data)

        return vector_dic

    # binary_file을 가공하여
    # vector로 반환
    def trim_data(self, bin_file):
        data = LoadData.unpickling(bin_file)
        data = self.interpolation(data)
        data = self.normalization(data)
        vector_data = self.vectorization(data)

        return vector_data

    # data를 입력받아
    # 일정한 INTERPOLATION_INTERVAL로 가공한 뒤,
    # list 형식으로 data 반환
    def interpolation(self, data):
        y = []

        minute_check = data['ts'][0][0].minute / self.INTERPOLATION_INTERVAL
        item = 0
        value_collector = 0

        for i in range(0, len(data['ts'])):
            if data['ts'][i][2] / self.INTERPOLATION_INTERVAL == minute_check:
                item += 1
                value_collector += data['value'][i]
            else:
                minute_check += 1
                if minute_check == 6:
                    minute_check = 0

                # 그 전 data value를 그대로 유지하는 strategy
                if item == 0:
                    y.append(y[-1])
                else:
                    y.append(value_collector / item)
                    value_collector = 0
                    item = 0
                i -= 1

        return y

    # list 형식의 data를 입력받아
    # SCALE_SIZE 범위 안으로 scaling 처리 한 뒤,
    # list 형식으로 data 반환
    def normalization(self, list):
        noise_filter = 10
        normalizer = self.n_th_maximum(noise_filter, list)

        if normalizer == 0:
            list_normalized = list
        else:
            list_normalized = np.array(list) / normalizer * self.SCALE_SIZE

        return list_normalized

    # list를 입력받아
    # 그 list의 n번째 최대값을
    # 반환
    def n_th_maximum(self, n_th, list):
        list_copy = copy.copy(list)
        list_copy.sort()
        return list_copy[-n_th]

    # list 형식의 data를 입력받아
    # VEC_DIMENSION의 차원으로 vector를 구성한 뒤,
    # list 형식으로 data 반환
    def vectorization(self, list):
        slicing_size = len(list) / self.VEC_DIMENSION
        vec = []
        vec_collector = 0

        for i in range(0, len(list)):
            vec_collector += list[i]
            if (i + 1) % slicing_size == 0:
                try:
                    vec.append(int(vec_collector / slicing_size))
                except ValueError:
                    # 0을 나누는 경우
                    vec.append(0)
                except OverflowError:
                    # 0으로 나누는 경우
                    vec.append(-1000)
                finally:
                    vec_collector = 0
        return vec


class Cluster:
    def __init__(self, AF_PREFERENCE):
        self.AF_PREFERENCE = AF_PREFERENCE

    # vector_dictionary를 입력받아
    # AffinityPropagation clustering을 통해
    # 각각의 vector들에 적합한 cluster를 구성한 뒤,
    # list형식의 cluster를 반환
    def affinity_propagation(self, vector_dic):
        vectors = vector_dic['vec_data']

        return AffinityPropagation(preference=self.AF_PREFERENCE).fit_predict(vectors)

    # vector_dictionary와 cluster를 입력받아
    # cluster_structure를 구성하여
    # dictionary 형식으로 반환
    def make_cluster_structure(self, vector_dic, clusters):
        cluster_structure = {}

        cluster_structure['file_name'] = vector_dic['file_name']
        cluster_structure['vec_data'] = vector_dic['vec_data']
        cluster_structure['cluster_tag'] = clusters

        return cluster_structure


class Classifier:
    def __init__(self):
        pass

    # cluster_structure를 입력받아
    # classifier를 구성 & 학습시켜
    # 반환

    def train_clf(self, cluster_structure):
        X = np.array(cluster_structure['vec_data'])
        Y = np.array(cluster_structure['cluster_tag'])

        clf = GaussianNB()
        # clf = BernoulliNB()
        # clf = MultinomialNB()
        clf.fit(X, Y)

        return clf


class ModelDependency:
    def __init__(self):
        pass

    def cluster2modeldependency(self, dictionary):
        names = dictionary['file_name']
        vectors = dictionary['vec_data']

        X = np.array(vectors)
        elements = len(X)
        nbrs = NearestNeighbors(n_neighbors=elements, algorithm='auto').fit(X)
        distances, indices = nbrs.kneighbors(X)

        dependency = np.zeros((elements, elements))

        for row in xrange(0, elements):
            for col in xrange(0, elements):
                dependency[row][indices[row][col]] = distances[row][col]

        model_dependency = self.dependency2dic(names, dependency)

        return model_dependency

    def dependency2dic(self, names, dependency):
        model_dependency = {}
        model_dependency['file_name'] = names
        model_dependency['dependency'] = dependency

        return model_dependency
