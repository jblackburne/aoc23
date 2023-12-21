import sys
from itertools import combinations
from collections import Counter

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

    return data


def p13a(data):
    totals = []
    for iarr, arr in enumerate(data):
        nrow, ncol = arr.shape
        idxdict = {}
        for irow, row in enumerate(arr):
            rowstr = "".join(row)
            idxs = idxdict.get((rowstr, "row"), [])
            idxs.append(irow)
            idxdict[(rowstr, "row")] = idxs
        for icol, col in enumerate(arr.T):
            colstr = "".join(col)
            idxs = idxdict.get((colstr, "col"), [])
            idxs.append(icol)
            idxdict[(colstr, "col")] = idxs

        # Look for mirror candidates and count how many rows or cols support them
        candidates = []
        for (_, rc), idxs in idxdict.items():
            if len(idxs) < 2:
                continue
            num = nrow if rc == "row" else ncol
            for i, j in combinations(idxs, 2):
                irc2 = i + j + 1
                if irc2 % 2 == 0:
                    candidates.append((rc, irc2 // 2, num))
        cand_support = Counter(candidates)

        # A candidate is a legit mirror iff its support is enough to reach the edge
        mirrors = [(rc, irc) for (rc, irc, nrc), supp in cand_support.items()
                   if supp == min(irc, nrc - irc)]

        # Return the sum of mirror columns plus 100 * sum of mirror rows
        totals.append(sum([irc if rc == "col" else 100 * irc for (rc, irc) in mirrors]))

    return sum(totals)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p13(lines)

    print("Problem 13a: {}".format(p13a(data)))
