import sys

import numpy as np


# Possible cell states
EMPTY = 0
SQUARE = 1
ROUND = 2


def ingest_p14(lines):
    data = []
    for line in lines:
        data.append([EMPTY if c == "." else
                     SQUARE if c == "#" else
                     ROUND for c in line.strip()])

    return np.array(data)


def tilt(data, direction):
    if direction not in list("NESW"):
        raise ValueError("Bad direction: {}. Must be in NESW".format(direction))
    nrow, ncol = data.shape

    def get(ipar, iperp):
        irow, icol = ((ipar, iperp) if direction == "N" else
                      (iperp, ncol - ipar - 1) if direction == "E" else
                      (nrow - ipar - 1, iperp) if direction == "S" else
                      (iperp, ipar) if direction == "W" else None)
        return irow, icol

    npar, nperp = (nrow, ncol) if direction in "NS" else (ncol, nrow)
    out = np.copy(data)
    for iperp in range(nperp):
        iparback = 0
        while True:
            while iparback < npar and out[get(iparback, iperp)] != EMPTY:
                iparback += 1
            iparfwd = iparback + 1
            while iparfwd < npar and out[get(iparfwd, iperp)] == EMPTY:
                iparfwd += 1
            if iparfwd >= npar:
                break
            if out[get(iparfwd, iperp)] == ROUND:
                out[get(iparfwd, iperp)] = EMPTY
                out[get(iparback, iperp)] = ROUND
                iparback += 1
            else:  # square boulder
                iparback = iparfwd

    return out


def p14a(data):
    nrow, ncol = data.shape
    tilted = tilt(data, "N")
    load = (np.arange(nrow, 0, -1)[:, np.newaxis] * (tilted == ROUND)).sum()

    return load


def p14b(data):
    spun = np.copy(data)
    cache = {}
    ispin = 0
    while ispin < 1000000000:
        # Try to find a cycle if we haven't already
        if cache is not None:
            key = tuple(spun.flat)
            prevspin = cache.get(key)
            if prevspin is not None:
                cycle_len = ispin - prevspin
                ispin += ((1000000000 - ispin) // cycle_len) * cycle_len
                cache = None
            else:
                cache[key] = ispin

        # Spin!
        spun = tilt(spun, "N")
        spun = tilt(spun, "W")
        spun = tilt(spun, "S")
        spun = tilt(spun, "E")
        ispin += 1

    nrow, ncol = spun.shape
    load = (np.arange(nrow, 0, -1)[:, np.newaxis] * (spun == ROUND)).sum()

    return load


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p14(lines)

    print("Problem 14a: {}".format(p14a(data)))
    print("Problem 14b: {}".format(p14b(data)))
