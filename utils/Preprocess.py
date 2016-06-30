# -*- coding: utf-8 -*-

import numpy as np
from GlobalParameter import *
import FileIO
import cmath as math
from datetime import timedelta
import cPickle as pickle
import os


def refining_data(time_interval=TimeInterval, refined_type=FullyPreprocessedPath):
    """
    - raw sensor data 를 preprocessing 과정을 통해 refined data 로 변환
    - refined data 를 time interval 별로 지정된 directory 에 저장
    - refined data repository directory 를 반환함

    :param time_interval:
        time interval for time scaling
    :param refined_type:
        refine type
    :return:
        refined data directory path
    """
    print 'time stamp standardization'
    ts_standardization()

    print 'data preprocess'
    for line in FileIO.Load.binary_file_list(os.path.join(RepositoryPath, TimeLengthStandardPath)):
        file_name = line.rsplit('/', 1)[-1]

        print '\t',
        print 'refining : ' + file_name

        if refined_type == FullyPreprocessedPath:
            _, refined_path = FileIO.Save.refined_data2bin_file(fully_data_preprocess(line, time_interval),
                                                                FullyPreprocessedPath, time_interval)
        elif refined_type == SemiPreprocessedPath:
            _, refined_path = FileIO.Save.refined_data2bin_file(
                skip_interpolation_data_preprocess(line, time_interval), SemiPreprocessedPath, time_interval)
        else:
            print "error occurred in preprocess"
            exit()

    return refined_path


###############################################################################
#

def ts_standardization():
    # load raw data binary file list
    repository_path = os.path.join(RepositoryPath, RawDataPath)
    raw_data_binary_file_list = FileIO.Load.binary_file_list(repository_path)

    # set temporary start ts & end ts
    start_ts, end_ts = set_ts_spectrum(raw_data_binary_file_list)

    print '\t',
    print 'synchronizing time stamp'
    for binary_file in raw_data_binary_file_list:
        data = pickle.load(open(binary_file))
        for i in xrange(0, len(data['ts'])):
            if start_ts <= data['ts'][i][0]:
                start_idx = i
                break
        for j in xrange(len(data['ts']) - 1, 0, -1):
            if end_ts >= data['ts'][j][0]:
                end_idx = j
                break

        data['ts'] = data['ts'][start_idx:end_idx + 1]
        data['value'] = data['value'][start_idx:end_idx + 1]
        data['ts'][0][0] = start_ts
        data['ts'][-1][0] = end_ts

        FileIO.Save.ts_standard_data2bin_file(data, binary_file.rsplit('/', 1)[-1])


def set_ts_spectrum(raw_data_binary_file_list):
    """

    :param raw_data_binary_file_list:
    :return:
    """
    data = pickle.load(open(raw_data_binary_file_list[0]))
    start_ts = data['ts'][0][0]
    end_ts = data['ts'][-1][0]

    print '\t',
    print 'searching latest start_ts & earliest end_ts...'

    for binary_file in raw_data_binary_file_list:
        data = pickle.load(open(binary_file))
        start_ts = max(start_ts, data['ts'][0][0])
        end_ts = min(end_ts, data['ts'][-1][0])

    start_ts = start_ts.replace(hour=0, minute=0, second=0)
    start_ts = start_ts + timedelta(days=1)
    end_ts = end_ts.replace(hour=0, minute=0, second=0)

    print '\t\t' + 'start_ts: ' + str(start_ts)
    print '\t\t' + 'end_ts: ' + str(end_ts)

    return start_ts, end_ts


###############################################################################
# Data Preprocess

def fully_data_preprocess(binary_file_path, time_interval=TimeInterval):
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


def skip_interpolation_data_preprocess(binary_file_path, time_interval=TimeInterval):
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

    # Standardize a data_set
    data_dictionary['value'] /= data_dictionary['value'].std()

    return data_dictionary


###############################################################################
# Time Stamp Scaling

def ts_scaling(dictionary_data, time_interval=TimeInterval):
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

if __name__ == '__main__':
    refining_data()
