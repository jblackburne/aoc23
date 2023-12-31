import sys

import numpy as np


N, E, S, W, ERR = range(5)
DELTA = ((-1, 0), (0, 1), (1, 0), (0, -1))


def ingest_p16(lines):
    out = []
    for line in lines:
        out.append(list(line.strip()))

    return np.array(out)


def p16a(data, irow=0, icol=0, direction=E):
    nrow, ncol = data.shape

    visited = np.zeros((4, nrow, ncol), dtype=bool)
    rays = [((irow, icol), direction)]
    while len(rays) > 0:
        (irow, icol), direction = rays.pop()
        while True:
            if not (0 <= irow < nrow and 0 <= icol < ncol):
                break
            if visited[direction, irow, icol]:
                break
            visited[direction, irow, icol] = True
            if data[irow, icol] == "\\":
                direction = (W if direction == N else
                             S if direction == E else
                             E if direction == S else
                             N if direction == W else ERR)
            elif data[irow, icol] == "/":
                direction = (E if direction == N else
                             N if direction == E else
                             W if direction == S else
                             S if direction == W else ERR)
            elif data[irow, icol] == "-":
                if direction in (N, S):
                    direction = E
                    rays.append(((irow, icol), W))
            elif data[irow, icol] == "|":
                if direction in (E, W):
                    direction = N
                    rays.append(((irow, icol), S))

            irow += DELTA[direction][0]
            icol += DELTA[direction][1]

    return np.logical_or.reduce(visited, axis=0).sum()


def p16b(data):
    nrow, ncol = data.shape
    sums = ([p16a(data, irow=irow, icol=0, direction=E) for irow in range(nrow)] +
            [p16a(data, irow=irow, icol=ncol-1, direction=W) for irow in range(nrow)] +
            [p16a(data, irow=0, icol=icol, direction=S) for icol in range(ncol)] +
            [p16a(data, irow=nrow-1, icol=icol, direction=N) for icol in range(ncol)])
    return max(sums)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p16(lines)

    print("Problem 16a: {}".format(p16a(data)))
    print("Problem 16b: {}".format(p16b(data)))
