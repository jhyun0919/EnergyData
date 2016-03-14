# contact: https://github.com/jeonghoonkang

import sys
import cPickle as pickle
import matplotlib

try:
	file_path = sys.argv[1]
except IndexError as err:
	print('IndexError: ' + str(err))
	print('Usage: python parsing <filename>')
	exit()

tsfile = pickle.load(open(file_path))

print
print "loading ... Bin file"

print tsfile
print

