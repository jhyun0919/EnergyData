# -*- coding: utf-8 -*-


def decalcomanie(matrix):
    if square_matrix(matrix):
        dimension = len(matrix)

        for row in xrange(0, dimension):
            for col in xrange(row + 1, dimension):
                matrix[col][row] = matrix[row][col]
    else:
        print 'given matrix is not squared matrix'
        exit()

    return matrix


def square_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    if rows == cols:
        return True
    else:
        return False
