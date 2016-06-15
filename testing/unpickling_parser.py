import cPickle as pickle
import sys

file_path = sys.argv[1]

data = pickle.load(open(file_path))

if __name__ == "__main__":

    for ts, value in zip(data['ts'], data['value']):
        print ts[0],
        print '\t',
        print value

