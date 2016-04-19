import cPickle as pickle


def parsing(file_path):
    vec_data = pickle.load(open(file_path))
    return vec_data
