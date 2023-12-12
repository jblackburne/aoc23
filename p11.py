import sys

import numpy as np


def ingest_p11(lines):
    data = []
    for line in lines:
        row = []
        for c in line.strip():
            row.append(c == "#")
        data.append(row)

    data = np.array(data)

    # Determine the row/col indices of galaxies (before expansion)
    galaxylocs = list(zip(*np.nonzero(data)))

    # Now determine rows and columns that need to expand
    nrow, ncol = data.shape
    rowempty = ~np.any(data, axis=1)
    colempty = ~np.any(data, axis=0)
    colpos = np.arange(ncol)
    rowpos = np.arange(nrow)
    colpos[1:] += np.cumsum(colempty)[:-1]
    rowpos[1:] += np.cumsum(rowempty)[:-1]

    return galaxylocs, rowpos, colpos


def p11a(galaxylocs, rowpos, colpos):
    ngal = len(galaxylocs)
    distances = []
    for j in range(ngal - 1):
        rowj = rowpos[galaxylocs[j][0]]
        colj = colpos[galaxylocs[j][1]]
        for i in range(j + 1, ngal):
            rowi = rowpos[galaxylocs[i][0]]
            coli = colpos[galaxylocs[i][1]]
            distances.append(abs(rowj - rowi) + abs(colj - coli))

    return np.sum(distances)


def p11b(galaxylocs, rowpos, colpos):
    # Since the expansion is much bigger, modify rowpos and colpos
    rowpos -= np.arange(len(rowpos))
    colpos -= np.arange(len(colpos))
    rowpos *= 999999
    colpos *= 999999
    rowpos += np.arange(len(rowpos))
    colpos += np.arange(len(colpos))

    ngal = len(galaxylocs)
    distances = []
    for j in range(ngal - 1):
        rowj = rowpos[galaxylocs[j][0]]
        colj = colpos[galaxylocs[j][1]]
        for i in range(j + 1, ngal):
            rowi = rowpos[galaxylocs[i][0]]
            coli = colpos[galaxylocs[i][1]]
            distances.append(abs(rowj - rowi) + abs(colj - coli))

    return np.sum(distances)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    galaxylocs, rowpos, colpos = ingest_p11(lines)

    print("Problem 11a: {}".format(p11a(galaxylocs, rowpos, colpos)))
    print("Problem 11b: {}".format(p11b(galaxylocs, rowpos, colpos)))
