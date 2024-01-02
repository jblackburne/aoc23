import sys
from queue import PriorityQueue

import numpy as np


N, E, S, W, UNBOUND = range(5)
DELTA = ((-1, 0), (0, 1), (1, 0), (0, -1))


def ingest_p17(lines):
    data = []
    for line in lines:
        data.append([int(c) for c in line.strip()])

    return np.array(data)

def p17a(data, min_straight=1, max_straight=3):
    nrow, ncol = data.shape
    begin = (0, 0)
    end = (nrow - 1, ncol - 1)

    # Needed for the algorithm below
    assert(N % 2 == S % 2 and E % 2 == W % 2)

    min_cost = np.full((nrow, ncol, 2), 1 << 30)
    tasks = PriorityQueue()
    for icol in range(min_straight, max_straight + 1):
        dest = (begin[0] + icol * DELTA[E][0], begin[1] + icol * DELTA[E][1])
        tasks.put_nowait((data[0, 1:icol].sum(), dest, E))
    for irow in range(min_straight, max_straight + 1):
        dest = (begin[0] + irow * DELTA[S][0], begin[1] + irow * DELTA[S][1])
        tasks.put_nowait((data[1:irow, 0].sum(), dest, S))
    while True:
        tot_cost, (irow, icol), direction = tasks.get_nowait()

        if not (0 <= irow < nrow and 0 <= icol < ncol):
            continue
        if min_cost[irow, icol, direction % 2] <= tot_cost:
            continue
        else:
            min_cost[irow, icol, direction % 2] = tot_cost
        tot_cost += data[irow, icol]

        if (irow, icol) == end:
            return tot_cost

        branches = (E, W) if direction in (N, S) else (N, S)
        for branch in branches:
            new_cost = tot_cost
            new_irow = irow
            new_icol = icol
            for i in range(1, max_straight + 1):
                new_irow += DELTA[branch][0]
                new_icol += DELTA[branch][1]
                if (0 <= new_irow < nrow and 0 <= new_icol < ncol):
                    if i >= min_straight:
                        tasks.put_nowait((new_cost, (new_irow, new_icol), branch))
                    new_cost += data[new_irow, new_icol]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p17(lines)

    print("Problem 17a: {}".format(p17a(data)))
    print("Problem 17b: {}".format(p17a(data, min_straight=4, max_straight=10)))
