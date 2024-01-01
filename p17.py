import sys
from queue import PriorityQueue

import numpy as np


N, E, S, W, ERR = range(5)
DELTA = ((-1, 0), (0, 1), (1, 0), (0, -1))


def ingest_p17(lines):
    data = []
    for line in lines:
        data.append([int(c) for c in line.strip()])

    return np.array(data)

# This implementation is probably buggy.  It will stop following a
# path if that path visits a square that another path has visited
# before with a lower total cost. But that previous path might have
# had a constraint preventing it from going a direction with lower
# future cost, a constraint this path does not have.
def p17a(data, max_straight=3):
    nrow, ncol = data.shape
    begin = (0, 0)
    end = (nrow - 1, ncol - 1)

    min_cost = np.full_like(data, 1 << 30)
    tasks = PriorityQueue()
    tasks.put_nowait((0, (begin[0] + DELTA[E][0], begin[1] + DELTA[E][1]), E))
    tasks.put_nowait((0, (begin[0] + DELTA[S][0], begin[1] + DELTA[S][1]), S))
    while tasks.qsize() > 0:
        tot_cost, (irow, icol), direction = tasks.get()
        for istep in range(max_straight):
            if not (0 <= irow < nrow and 0 <= icol < ncol):
                break
            tot_cost += data[irow, icol]
            if tot_cost < min_cost[irow, icol]:
                min_cost[irow, icol] = tot_cost
            else:
                break

            branches = (E, W) if direction in (N, S) else (N, S)
            for branch in branches:
                step = DELTA[branch]
                tasks.put_nowait((tot_cost, (irow + step[0], icol + step[1]), branch))

            step = DELTA[direction]
            irow += step[0]
            icol += step[1]

    # Now the min cost at the end is the answer
    return min_cost[end]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p17(lines)

    print("Problem 17a: {}".format(p17a(data)))
