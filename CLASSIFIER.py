from sklearn.naive_bayes import GaussianNB
# from sklearn.naive_bayes import BernoulliNB
# from sklearn.naive_bayes import MultinomialNB
from DATA2VEC import *
from VEC2CLUSTER import CLUSTER_STRUCTURE_NAME
from VEC2CLUSTER import bin2graph


def train_clf(cluster_structure):
    X = np.array(cluster_structure['vector'])
    Y = np.array(cluster_structure['cluster_tag'])

    clf = GaussianNB()
    # clf = BernoulliNB()
    # clf = MultinomialNB()
    clf.fit(X, Y)

    return clf


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), RESULT_DIRECTORY, CLUSTER_STRUCTURE_NAME)
    cluster_structure = unpickling(file_path)

    print cluster_structure

    clf = train_clf(cluster_structure)

    print clf.predict(trim_data(sys.argv[1]))
    bin2graph(sys.argv[1])
