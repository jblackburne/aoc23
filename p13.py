import sys

import numpy as np


def ingest_p13(lines):
    data = []
    current = []
    for line in lines:
        if line.strip() == "":
            data.append(np.array(current))
            current = []
        else:
            current.append(list(line.strip()))

    if len(current) > 0:
        data.append(np.array(current))

    return data


def p13a(data, nsmudges=0):
    totals = []
    for arr in data:
        nrow, ncol = arr.shape

        # Calculate pairwise Hamming distances between pairs of rows and
        # pairs of columns
        # These (n x n) arrays will have diagonals of zeros running SW to NE
        # when there are mirrors
        rowham = np.array([[np.count_nonzero(arr[i] != arr[j])
                            for i in range(nrow)] for j in range(nrow)])
        colham = np.array([[np.count_nonzero(arr[:, i] != arr[:, j])
                            for i in range(ncol)] for j in range(ncol)])

        rowmirrors = np.nonzero([np.trace(rowham[::-1], offset=i) == 2 * nsmudges
                                 for i in range(-nrow+2, nrow-1, 2)])[0] + 1
        colmirrors = np.nonzero([np.trace(colham[::-1], offset=i) == 2 * nsmudges
                                 for i in range(-ncol+2, ncol-1, 2)])[0] + 1

        totals.append(rowmirrors.sum() * 100 + colmirrors.sum())

    return sum(totals)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p13(lines)

    print("Problem 13a: {}".format(p13a(data)))
    print("Problem 13b: {}".format(p13a(data, nsmudges=1)))
