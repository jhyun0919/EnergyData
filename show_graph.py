# -*- coding: utf-8 -*-
# contact: https://github.com/jeonghoonkang

import sys
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt


# Load Data

def load_file():
	try:
		# file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT/VTT_GW1_HA2_VM_EP_KV_K.bin'
		file_path = sys.argv[1]
	except IndexError as err:
		print('IndexError: ' + str(err))
		exit()
	data = pickle.load(open(file_path))
	return data


# # Plot Data
#
# x, y = [], []
#
# for line in time_stamp:
# 	x.append(line[0])
#
# for line in value:
# 	y.append(line)
#
# for i in range(0, len(x)):
# 	print(x[i]),
# 	print('\t value: %d' %y[i])
#
# plt.plot(x,y,linestyle = '-', marker = 'x', label = "value")
#
# plt.xlabel('time')
# plt.legend(loc = 2)
# plt.show()

def draw_graph(y):
	i = np.linspace(0, 1, len(y))
	plt.scatter(i, y, marker='x')
	plt.show()

	# plt.savefig('foo.jpg')


if __name__ == "__main__":
	data = load_file()
	draw_graph(data['value'])