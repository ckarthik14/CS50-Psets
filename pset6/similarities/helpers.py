from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


# returns a tuple for location (i, j)
def minimum(matrix, i, j, x):
    if matrix[i - 1][j][0] < matrix[i][j - 1][0]:
        if matrix[i - 1][j][0] + 1 < matrix[i - 1][j - 1][0] + x:
            return (matrix[i - 1][j][0] + 1, Operation.DELETED)
        else:
            return (matrix[i - 1][j - 1][0] + x, Operation.SUBSTITUTED)

    else:
        if matrix[i][j - 1][0] + 1 < matrix[i - 1][j - 1][0] + x:
            return (matrix[i][j - 1][0] + 1, Operation.INSERTED)
        else:
            return (matrix[i - 1][j - 1][0] + x, Operation.SUBSTITUTED)


def distances(a, b):
    """Calculate edit distance from a to b"""

    # initialize two lists
    matrix = []
    temp = []

    # append the first row
    for i in range(len(b) + 1):
        if i == 0:
            temp.append((i, None))
        else:
            temp.append((i, Operation.INSERTED))

    matrix.append(temp[:])

    # making list empty
    temp[:] = []

    # initialize first element of every row
    for i in range(1, len(a) + 1):
        temp.append((i, Operation.DELETED))
        matrix.append(temp[:])
        temp[:] = []

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            # finding value of x
            if a[i - 1] == b[j - 1]:
                x = 0
            else:
                x = 1

            # getting cost for (i, j)
            cost = minimum(matrix, i, j, x)
            matrix[i].append(cost)

    return matrix
