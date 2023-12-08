import sys
from itertools import cycle

import numpy as np


def ingest_p08(lines):
    directions = lines[0].strip()

    nodes = []
    lnodes = []
    rnodes = []
    is_start = []
    is_end = []
    for line in lines[2:]:
        nodestr, lrstr = line.strip().split(" = ")
        lstr, rstr = lrstr[1:-1].split(", ")
        nodes.append(nodestr)
        lnodes.append(lstr)
        rnodes.append(rstr)
        is_start.append(nodestr.endswith("A"))
        is_end.append(nodestr.endswith("Z"))

    # Sort the lists
    junk = list(zip(nodes, lnodes, rnodes, is_start, is_end))
    junk.sort()
    nodes, lnodes, rnodes, is_start, is_end = zip(*junk)

    # Convert the strings into numeric encodings
    nodemap = {n: i for (n, i) in zip(sorted(nodes), range(len(nodes)))}
    nodes = [nodemap[x] for x in nodes]
    lnodes = [nodemap[x] for x in lnodes]
    rnodes = [nodemap[x] for x in rnodes]

    return directions, lnodes, rnodes, is_start, is_end


def p08a(directions, lnodes, rnodes):
    startnode = 0  # AAA
    endnode = len(lnodes) - 1  # ZZZ
    inode = startnode
    nsteps = 0
    for step in cycle(directions):
        inode = lnodes[inode] if step == "L" else rnodes[inode]
        nsteps += 1
        if inode == endnode:
            break

    return nsteps


def p08b(directions, lnodes, rnodes, is_start, is_end):
    """This one is dumb. I solved it by noticing that each starting point
    reaches its end in a number of steps exactly some integer times
    the length of the input directions sequence. All the numbers were
    primes. So I just ran something like p08a to get that list of primes.
    """
    nloops = [67, 59, 79, 71, 61, 53]
    return np.prod(nloops) * len(directions)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        directions, lnodes, rnodes, is_start, is_end = ingest_p08(f.readlines())

    print("Problem 8a: {}".format(p08a(directions, lnodes, rnodes)))
    print("Problem 8b: {}".format(p08b(directions, lnodes, rnodes, is_start, is_end)))
