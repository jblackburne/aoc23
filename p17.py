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

def p17a(data, max_straight=3):
    nrow, ncol = data.shape
    begin = (0, 0)
    end = (nrow - 1, ncol - 1)

    min_cost = np.full((nrow, ncol, 5), 1 << 30)
    tasks = PriorityQueue()
    tasks.put_nowait((0, (begin[0] + DELTA[E][0], begin[1] + DELTA[E][1]), E))
    tasks.put_nowait((0, (begin[0] + DELTA[S][0], begin[1] + DELTA[S][1]), S))
    while tasks.qsize() > 0:
        tot_cost, (irow, icol), direction = tasks.get()
        for istep in range(max_straight):
            if not (0 <= irow < nrow and 0 <= icol < ncol):
                break
            tot_cost += data[irow, icol]
            if istep == max_straight - 1:
                # Bounded in one direction. Stop if another path
                # bounded in this direction or unbounded has an equal
                # or lower min cost. Otherwise set this direction's
                # min cost
                if (min_cost[irow, icol, UNBOUND] <= tot_cost or
                    min_cost[irow, icol, direction] <= tot_cost):
                    break
                min_cost[irow, icol, direction] = tot_cost
            else:
                # Unbounded. Stop if another unbounded path has an
                # equal or lower min cost. Otherwise set the unbounded
                # min cost
                if min_cost[irow, icol, UNBOUND] <= tot_cost:
                    break
                min_cost[irow, icol, UNBOUND] = tot_cost

            branches = (E, W) if direction in (N, S) else (N, S)
            for branch in branches:
                step = DELTA[branch]
                tasks.put_nowait((tot_cost, (irow + step[0], icol + step[1]), branch))

            step = DELTA[direction]
            irow += step[0]
            icol += step[1]

    # Now the min cost at the end is the answer
    return np.min(min_cost[end])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p17(lines)

    print("Problem 17a: {}".format(p17a(data)))
