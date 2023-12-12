import sys

import numpy as np


def ingest_p10(lines):
    data = []
    for irow, line in enumerate(lines):
        row = []
        for icol, c in enumerate(line.strip()):
            row.append(1 if c == "-" else
                       -1 if c == "|" else
                       -1j if c in "JF" else
                       1j if c in "7L" else
                       0)
            if c == "S":
                startidx = (irow, icol)
                startdata = [l[icol-1:icol+2] for l in lines[irow-1:irow+2]]
        data.append(row)
    data = np.array(data)

    # Now determine the possible starting directions
    startdirs = []
    if startdata[1][0] in "-FL":
        startdirs.append(-1)
    if startdata[1][2] in "-J7":
        startdirs.append(1)
    if startdata[0][1] in "|F7":
        startdirs.append(-1j)
    if startdata[2][1] in "|JL":
        startdirs.append(1j)
    assert(len(startdirs) == 2)

    # And because it may be important, populate the starting point
    # with the right phasor
    sdir = set(startdirs)
    data[startidx] = (1 if sdir == {1, -1} else
                      -1 if sdir == {1j, -1j} else
                      -1j if sdir == {-1, 1j} else
                      -1j if sdir == {1, -1j} else
                      1j if sdir == {-1, -1j} else
                      1j if sdir == {1, 1j} else
                      0)
    startchar = ("-" if sdir == {1, -1} else
                 "|" if sdir == {1j, -1j} else
                 "7" if sdir == {-1, 1j} else
                 "L" if sdir == {1, -1j} else
                 "J" if sdir == {-1, -1j} else
                 "F" if sdir == {1, 1j} else
                 ".")

    return data, startidx, startdirs, startchar


def p10a(data, startidx, startdirs):
    irow, icol = startidx
    d = startdirs[0]  # arbitrary
    nsteps = 0
    done = False
    while not done:
        irow += int(d.imag)
        icol += int(d.real)
        nsteps += 1
        d = np.conj(d) * data[irow, icol]
        if (irow, icol) == startidx:
            done = True

    return nsteps // 2


def p10b(lines, data, startidx, startdirs, startchar):
    """An interior (exterior) point will have an odd (even) number of loop
    edges between it and the edge of the array. We count from the left
    side of the array, so we are counting vertical edges. Note that
    loop corners necessitate keeping separate track of top and bottom
    "halves" of the edge. For example, L and J have a top half, and F
    and 7 have bottom halves.
    """
    # Replace "S" with the real starting character
    irow, icol = startidx
    lines[irow] = lines[irow].replace("S", startchar)

    # Traverse the loop, keeping track of how many top/bottom half
    # edges there are
    nedge = np.zeros(data.shape + (2,), dtype=int)
    d = startdirs[0]  # arbitrary
    done = False
    while not done:
        c = lines[irow][icol]
        if c in "LJ|": nedge[irow, icol, 0] += 1
        if c in "7F|": nedge[irow, icol, 1] += 1
        if c == "-": nedge[irow, icol] += 2  # these are ineligible for being inside
        irow += int(d.imag)
        icol += int(d.real)
        d = np.conj(d) * data[irow, icol]
        if (irow, icol) == startidx:
            done = True

    # Now our nedge array tells us how many edges there are in the
    # loop to the left of any square
    inloop = np.logical_or.reduce(nedge > 0, axis=-1)
    nedgeleft = np.cumsum(nedge, axis=1)
    interior = np.logical_and(~inloop, np.logical_and.reduce(nedgeleft % 2, axis=-1))

    return np.sum(interior)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data, startidx, startdirs, startchar = ingest_p10(lines)

    print("Problem 10a: {}".format(p10a(data, startidx, startdirs)))
    print("Problem 10b: {}".format(p10b(lines, data, startidx, startdirs, startchar)))
