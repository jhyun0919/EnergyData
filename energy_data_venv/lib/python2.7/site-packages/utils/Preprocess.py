# -*- coding: utf-8 -*-

import Graph
import numpy as np
from GlobalParameter import *
import FileIO
import cmath as math
import time
from datetime import timedelta


def refining_data(raw_data_repository_path=Raw_Data_Repository_Path,
                  time_interval=Time_Interval):
    """
    - raw sensor data 를 preprocessing 과정을 통해 refined data 로 변환
    - refined data 를 time interval 별로 지정된 directory 에 저장
    - refined data repository directory 를 반환함

    :param raw_data_repository_path:
        row data repository directory
    :param time_interval:
        time interval for time scaling
    :return:
        refined data directory path
    """
    for line in FileIO.Load.binary_file_list(raw_data_repository_path):
        file_name = line.rsplit('/', 1)[-1]

        print 'refining : ',
        print file_name
        print '\t' + 'with ts_interval ' + str(time_interval) + ' min'

        start_time = time.time()

        _, fully_refined_path = FileIO.Save.refined_data2bin_file(fully_data_preprocess(line, time_interval),
                                                                  Fully_Preprocessed_Path, time_interval)
        _, skip_interpolation_path = FileIO.Save.refined_data2bin_file(
            skip_interpolation_data_preprocess(line, time_interval), Semi_Preprocessed_Path, time_interval)

        end_time = time.time()
        run_time = end_time - start_time

        print '\t' + 'run_time: ' + str(run_time) + ' sec'

    return fully_refined_path, skip_interpolation_path


###############################################################################
# Data Preprocess

def fully_data_preprocess(binary_file_path, time_interval=Time_Interval):
    """
    - 일정한 크기로 data 값을 scaling 함
    - 시간 간격을 일정하게 조정
    - 비어있는 곳에 적당한 값을 interpolate

    :param binary_file_path:
        energy data file 의 path
        - type: string
    :param time_interval:
        time_scaling 의 argument 로 전달
        - type: integer
    :return:
        preprocessing 된 energy data
        - type: dictionary
    """
    raw_data = FileIO.Load.unpickling(binary_file_path)
    refined_data = interpolation(ts_scaling(scaling(raw_data), time_interval))

    return refined_data


def skip_interpolation_data_preprocess(binary_file_path, time_interval=Time_Interval):
    """
    - 일정한 크기로 data value 값을 scaling 함
    - 시간 간격을 일정하게 조정

    :param binary_file_path:
        energy data file 의 path
        - type: string
    :param time_interval:
        time_scaling 의 argument 로 전달
        - type: integer
    :return:
        preprocessing 된 energy data
        - type: dictionary
    """
    raw_data = FileIO.Load.unpickling(binary_file_path)
    semi_refined_data = ts_scaling(scaling(raw_data), time_interval)

    return semi_refined_data


###############################################################################
# Value Scaling

def scaling(data_dictionary):
    """
    - scaling 을 해주는 함수
    - Global_Parameter 에서 정의된 Scale_Size 에 따라 scaling 실행

   :param data_dictionary:
        original_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    :return:
        scaled_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    """

    # sklearn.preprocessing.scale

    # Standardize a dataset along any axis
    # Center to the mean
    # Component wise scale to unit variance.

    # data_dictionary['value'] = scale(data_dictionary['value'], axis=0, with_mean=True, with_std=True, copy=True)
    data_dictionary['value'] /= data_dictionary['value'].std()

    return data_dictionary


###############################################################################
# Time Stamp Scaling

def ts_scaling(dictionary_data, time_interval=Time_Interval):
    """
    - ts 간격을 같게 변환 해주는 함수

    :param dictionary_data:
        original_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    :param time_interval:

    :return:
        interpolated_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    """

    # 새로 만들어질 time_stamp 와 value
    ts = []
    value = []

    # time stamp shifting window 설정
    present_ts = dictionary_data['ts'][0][0].replace(second=0)
    minute_scanner = dictionary_data['ts'][0][0].minute / time_interval
    present_ts = present_ts.replace(minute=minute_scanner * time_interval)
    ts_delta = timedelta(minutes=time_interval)
    next_ts = present_ts + ts_delta

    # 일정한 interval 로 time stamp 를 조정하고
    # 각 ts 에 적당한 value 값을 계산하여 배정함
    value_collector = []
    for i in range(0, len(dictionary_data['ts'])):
        if dictionary_data['ts'][i][0] < next_ts:
            value_collector.append(dictionary_data['value'][i])
        else:
            ts.append(present_ts)

            calculated_value = sum(value_collector) / len(value_collector)
            del value_collector[:]
            value.append(calculated_value)

            present_ts = next_ts
            next_ts = present_ts + ts_delta

            nan_number = ts_validity_checker(present_ts, dictionary_data['ts'][i][0], ts_delta)

            for i_nan in xrange(0, nan_number):
                ts.append(present_ts)
                value.append(np.nan)

                present_ts = next_ts
                next_ts = present_ts + ts_delta

            value_collector.append(dictionary_data['value'][i])

        # for final ts & value
        if i == (len(dictionary_data['ts']) - 1):
            ts.append(present_ts)
            calculated_value = sum(value_collector) / len(value_collector)
            value.append(calculated_value)

    # 최적화를 위해 list 를 np.array 로 변경
    dictionary_data['ts'] = np.array(ts)
    dictionary_data['value'] = np.array(value)

    return dictionary_data


def ts_validity_checker(present_ts, ts_index, ts_delta):
    """

    :param present_ts:
    :param ts_index:
    :param ts_delta:
    :return:
    """
    validity_number = 0
    next_ts = present_ts + ts_delta
    while True:
        if next_ts >= ts_index:
            break
        elif next_ts < ts_index:
            validity_number += 1
            next_ts = next_ts + ts_delta

    return validity_number


###############################################################################
# Value Interpolation

def interpolation(data_dictionary):
    """
    - nan 이 존재하는 data 를 interpolation 해주는 함수

    :param data_dictionary:
        nan 이 존재하는 data_dictionary
        - type: dictionary
    :return:
        nan 이 interpolate 된 data_dictionary
        - type: dictionary
    """
    for i in xrange(0, len(data_dictionary['value'])):
        if math.isnan(data_dictionary['value'][i]):
            data_dictionary['value'][i] = interpolation_rule(i, data_dictionary['value'])

    return data_dictionary


def interpolation_rule(idx, value):
    """
    - 감지된 nan 에 정해진 규칙에 따라 적당한 interpolation 값을 계산하여 반환해주는 함수

    :param idx:
        nan 의 index
        - type: integer
    :param value:
        value data
        - type: np.array
            - shape: (length, 1)
    :return:
        계산된 interpolation 값
        - type: float
    """
    denominator = 1

    for i in xrange(idx, len(value)):
        if math.isnan(value[i]):
            denominator += 1
        else:
            nominator = value[i] - value[idx - 1]
            break

    interpolated_value = value[idx - 1] + nominator / denominator

    return interpolated_value


###############################################################################
# Data-Preprocessing 4 Similarity

def ts_synchronize(binary_file_1, binary_file_2):
    """
    - 두 data 사이 similarity 를 계산하기 위해 ts 시작과 끝을 일치 시키는 함수
    - 공통된 ts 부분만 남기고 나머지 부분들은 삭제
    - 공통된 ts 부분의 value 값만 남긴다

    :param binary_file_1:
        binary file abs_path
    :param binary_file_2:
        binary file abs_path
    :return:
    """
    data_dictionary_1 = FileIO.Load.unpickling(binary_file_1)
    data_dictionary_2 = FileIO.Load.unpickling(binary_file_2)

    early, late = start_time_compare(data_dictionary_1, data_dictionary_2)
    early, late = start_ts_synchronize(early, late)
    early, late, length = end_ts_synchronize(early, late)

    return early['value'], late['value'], length


def start_time_compare(data_dictionary_1, data_dictionary_2):
    """
    - 시작 ts 값으로 early, late data  로 구분하여 반환

    :param data_dictionary_1:
    :param data_dictionary_2:
    :return:
    """
    if data_dictionary_1['ts'][0] > data_dictionary_2['ts'][0]:
        late = data_dictionary_1
        early = data_dictionary_2
    elif data_dictionary_1['ts'][0] < data_dictionary_2['ts'][0]:
        late = data_dictionary_2
        early = data_dictionary_1
    else:
        late = data_dictionary_1
        early = data_dictionary_2

    return early, late


def start_ts_synchronize(early, late):
    """
    - start time stamp 값을 통일시켜 반환

    :param early:
    :param late:
    :return:
    """
    for i in xrange(0, len(early['ts'])):
        if late['ts'][0] == early['ts'][i]:
            ts_fix = i
            break

    early['ts'] = early['ts'][ts_fix:]
    early['value'] = early['value'][ts_fix:]

    return early, late


def end_ts_synchronize(early, late):
    """
    - end time stamp 값을 통일시켜 반환

    :param early:
    :param late:
    :return:
    """
    if len(late['ts']) >= (len(early['ts'])):
        length = len(early['ts'])
        late['ts'] = late['ts'][0:length]

    else:
        length = len(late['ts'])
        early['ts'] = early['ts'][0:length]

    return early, late, length


"""
    X = X/X.std 로 바꿀 것..
"""


def preprocess4similarity_matrix(similarity_matrix):
    """
    -

    :param similarity_matrix:
    :return:
    """
    max_val = np.amax(similarity_matrix)
    min_val = np.amin(similarity_matrix)

    for i in xrange(0, len(similarity_matrix)):
        for j in xrange(0, len(similarity_matrix)):
            similarity_matrix[i][j] = (float(similarity_matrix[i][j] - min_val) / max_val) * Similarity_Matrix_Scaling

    return similarity_matrix


###############################################################################

if __name__ == '__main__':
    file_path = '/repository/VTT/VTT_GW1_HA11_VM_KV_K.bin'

    Graph.Show.raw_data2graph(file_path)

    data_dictionary = FileIO.Load.unpickling(file_path)

    data_dictionary = scaling(data_dictionary)
    print data_dictionary
    print
    Graph.Show.dictionary2graph(data_dictionary)

    data_dictionary = ts_scaling(data_dictionary)
    print data_dictionary
    print
    Graph.Show.dictionary2graph(data_dictionary)

    data_dictionary = interpolation(data_dictionary)
    print data_dictionary
    print
    Graph.Show.dictionary2graph(data_dictionary)
