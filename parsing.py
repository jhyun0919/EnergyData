# contact: https://github.com/jeonghoonkang

import cPickle as pickle
import sys


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

print "keys of %s" %file_path
print tsfile.keys()
print

"""
print "tsfile['ts'][0]"
print tsfile['ts'][0]
print

print "tsfile['ts'][1]"
print tsfile['ts'][1]
print

print "tsfile['ts'][2]"
print tsfile['ts'][2]
print

print "tsfile['ts'][10]"
print tsfile['ts'][10]
print
"""

for i in range(0, 100):
	print "tsfile['ts'][%d]" %i
	print tsfile['ts'][i]
	print

print "tsfile['value'][0]"
print tsfile['value'][0]
print

print "tsfile['value'][-1]"
print tsfile['value'][-1]
print

print "length of key ts is %d" % len(tsfile['ts'])

