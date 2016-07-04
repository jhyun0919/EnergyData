# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import cmath as math
import cPickle as pickle
from GlobalParameter import *
from GlobalParameter import *
import FileIO
from sklearn.preprocessing import scale


###############################################################################
# Data Preprocess

def data_preprocess(binary_file_path):
    """
    - 시간 간격을 일정하게 조정하고,
      비어있는 곳에 적당한 값을 interpolate 해주고,
      일정한 크기로 data 값을 scaling 함
    - 이웃한 time stamp 사이 value 의 변화량을 기록

    :param binary_file_path:
        energy data file 의 path
        - type: string
    :return:
        preprocessing 된 energy data
        - type: dictionary
    """
    # Load File and Unpickling
    dictionary_data = FileIO.Load.unpickling(binary_file_path)

    # Interval Equalization & Interpolation
    dictionary_data = interpolation(interval_equalization(dictionary_data))
    #
    # # Scaling
    # dictionary_data = scaling(dictionary_data)
    #
    # # Insert Instantaneous Value
    # dictionary_data['instantaneous_value'] = instantaneous_value(dictionary_data['value'])

    return dictionary_data


###############################################################################
# Interval Equalization

def interval_equalization(dictionary_data):
    """
    - ts 간격을 같게 변환 해주는 함수

    :param dictionary_data:
        original_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    :return:
        interpolated_dictionary = {"ts": ..., "value": ...}
        - type: dictionary
    """

    # 새로 만들어질 time_stamp 와 value
    ts = []
    value = []

    # time stamp shifting window 설정
    present_ts = dictionary_data['data_frame']['ts'][0].replace(second=0)
    minute_scanner = dictionary_data['data_frame']['ts'][0].minute / Time_Interval
    present_ts = present_ts.replace(minute=minute_scanner * Time_Interval)
    next_ts = present_ts + ts_delta

    # 일정한 interval 로 time stamp 를 조정하고
    # 각 ts 에 적당한 value 값을 계산하여 배정함
    value_collector = []
    for i in range(0, len(dictionary_data['data_frame']['ts'])):
        if dictionary_data['data_frame']['ts'][i] < next_ts:
            value_collector.append(dictionary_data['data_frame']['value'][i])
        else:
            ts.append(present_ts)

            calculated_value = sum(value_collector) / len(value_collector)
            del value_collector[:]
            value.append(calculated_value)

            present_ts = next_ts
            next_ts = present_ts + ts_delta

            nan_number = ts_validity_checker(present_ts, dictionary_data['data_frame']['ts'][i])

            for i_nan in xrange(0, nan_number):
                ts.append(present_ts)
                value.append(np.nan)

                present_ts = next_ts
                next_ts = present_ts + ts_delta

            value_collector.append(dictionary_data['data_frame']['value'][i])

        # for final ts & value
        if i == (len(dictionary_data['data_frame']['ts']) - 1):
            ts.append(present_ts)
            calculated_value = sum(value_collector) / len(value_collector)
            value.append(calculated_value)

    # 최적화를 위해 list 를 np.array 로 변경
    data = {}
    data['ts'] = np.array(ts)
    data['value'] = np.array(value)

    dictionary_data['data_frame'] = pd.DataFrame(data)

    return dictionary_data


def ts_validity_checker(present_ts, ts_index):
    """

    :param present_ts:

    :param ts_index:

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
# Interpolation

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
    for i in xrange(0, len(data_dictionary['data_frame']['value'])):
        if math.isnan(data_dictionary['data_frame']['value'][i]):
            data_dictionary['data_frame']['value'][i] = interpolation_rule(i, data_dictionary['data_frame']['value'])

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




if __name__ == '__main__':
    file_path = '/repository/VTT/VTT_GW1_HA11_VM_KV_KAM.bin'
    data_dictionary = data_preprocess(file_path)

    print data_dictionary

