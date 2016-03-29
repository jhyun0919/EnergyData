import cPickle as pickle
import sys

file_path = sys.argv[1]

vec_data = pickle.load(open(file_path))

print vec_data