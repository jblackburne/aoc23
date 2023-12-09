import sys

import numpy as np
from numpy.linalg import matrix_power


def p09a(data):
    nseries, n = np.shape(data)
    diffmat = np.diag(np.full(n, 1)) + np.diag(np.full(n - 1, -1), k=-1)
    diffmat[0, 0] = 0
    difftens = np.array([matrix_power(diffmat, i) for i in range(n)])

    diffs = np.einsum("ijk,mk->mij", difftens, data)
    predictions = diffs[:, :, -1].sum(axis=-1)

    return predictions.sum()


def p09b(data):
    nseries, n = np.shape(data)
    diffmat = np.diag(np.full(n, 1)) + np.diag(np.full(n - 1, -1), k=1)
    diffmat[-1, -1] = 0
    difftens = np.array([matrix_power(diffmat, i) for i in range(n)])

    diffs = np.einsum("ijk,mk->mij", difftens, data)
    predictions = diffs[:, :, 0].sum(axis=-1)

    return predictions.sum()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    data = np.loadtxt(sys.argv[1], dtype=int)

    print("Problem 9a: {}".format(p09a(data)))
    print("Problem 9b: {}".format(p09b(data)))
