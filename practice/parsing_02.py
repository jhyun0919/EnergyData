import cPickle as pickle
import sys

# file_path = sys.argv[1]
file_path = '/Users/JH/Documents/GitHub/EnergyData_jhyun/vector.bin'

vec_data = pickle.load(open(file_path))

names = vec_data['file_name']
vectors = vec_data['data']


if __name__ == "__main__":

    print vec_data

    # for name in names:
    #     print name
    #
    # for vector in vectors:
    #     print vector