# contact: https://github.com/jeonghoonkang

import sys
import cPickle as pickle
import matplotlib.pyplot as plt


# Load Data

try:
	file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/VTT/VTT_GW1_HA2_VM_EP_KV_K.bin'
		#sys.argv[1]
except IndexError as err:
	print('IndexError: ' + str(err))
	print('Usage: python parsing <filename>')
	exit()

data = pickle.load(open(file_path))
time_stamp = data['ts']
value = data['value']

print(time_stamp)
print(value)

# Plot Data

x, y = [], []

for line in time_stamp:
	x.append(line[0])

for line in value:
	y.append(line)

for i in range(0, len(x)):
	print(x[i]),
	print('\t value: %d' %y[i])








plt.plot(x,y,linestyle = '-', marker = 'x', label = "value")

plt.xlabel('time')
plt.legend(loc = 2)
plt.show()
