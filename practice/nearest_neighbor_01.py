from sklearn.neighbors import NearestNeighbors
import numpy as np
import time

start_time = time.time()

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1]])
nbrs = NearestNeighbors(n_neighbors=len(X), algorithm='auto').fit(X)

distances, indices = nbrs.kneighbors(X)

print 'indices'
print indices
print type(indices)
print

print 'distances'
print distances
print type(distances)
print


elements = len(X)
dependency = np.zeros((elements, elements))

for row in xrange(0, elements):
    for col in xrange(0, elements):
        dependency[row][indices[row][col]] = distances[row][col]

print 'dependency'
print dependency

end_time = time.time()

print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
