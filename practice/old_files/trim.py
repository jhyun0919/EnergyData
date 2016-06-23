# -*- coding: utf-8 -*-

import sys
import cPickle as pickle
import copy
import matplotlib.pyplot as plt

# Load Data

try:
    file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT/VTT_GW1_HA2_VM_EP_KV_K.bin'
    # file_path = sys.argv[1]
except IndexError as err:
    print('IndexError: ' + str(err))
    print('Usage: python parsing <filename>')
    exit()

data = pickle.load(open(file_path))
time_stamp = data['ts']
value = data['value']

print
print(data)

print
print('total length: ' + str(len(time_stamp)))

x, y = [], []

minute_checker = time_stamp[0][0].minute / 10
item = 0
value_temp = 0

for i in range(0, len(time_stamp)):
    if time_stamp[i][2] / 10 == minute_checker:
        item += 1
        value_temp += value[i]
    else:
        x.append(time_stamp[i - 1][0].replace(minute=10 * minute_checker, second=0))

        minute_checker += 1
        if minute_checker == 6:
            minute_checker = 0

        if item == 0:
            y.append(y[-1])
        else:
            y.append(value_temp / item)
            value_temp = 0
            item = 0

        i = i - 1

print
print('######### trimmed ##########')
print

for i in range(0, 5):
    print('ts: ' + str(x[i])),
    print('\tvalue: %d' % y[i])

print('.\n.\n.')

for i in xrange(len(x) - 5, len(x) - 1):
    print('ts: ' + str(x[i])),
    print('\tvalue: %d' % y[i])

print
print('total length: ' + str(len(x)))
print(float(len(x)) / len(time_stamp))

y_temp = copy.copy(y)
y_temp.sort()
y_max = y_temp[-100]
print('y_max: ' + str(y_max))

for i in range(0, len(y)):
    y[i] = (y[i] / y_max) * 100

plt.scatter(x, y, marker='x', label="value")

plt.xlabel('time')
plt.legend(loc=2)
plt.show()
