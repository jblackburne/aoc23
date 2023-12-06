import sys


class RangeMap:
    def __init__(self, from_begin=(), to_begin=(), num=()):
        if len(from_begin) != len(to_begin) or len(to_begin) != len(num):
            raise ValueError("Mismatched lengths!")

        self.from_begin = from_begin
        self.to_begin = to_begin
        self.num = num

    def __call__(self, from_val):
        to_val = None
        for fb, tb, n in zip(self.from_begin, self.to_begin, self.num):
            if fb <= from_val < fb + n:
                to_val = tb + from_val - fb
        if to_val is None:
            to_val = from_val

        return to_val


def ingest_p05(lines):
    # Just hard-code this crap
    seeds = [int(x) for x in lines[0].strip().split()[1:]]

    steps = [
        "seed",
        "soil",
        "fertilizer",
        "water",
        "light",
        "temperature",
        "humidity",
        "location",
    ]
    mapheaders = ["{}-to-{} map:\n".format(steps[i], steps[i + 1])
                  for i in range(len(steps) - 1)]
    mapheaderidx = [lines.index(x) for x in mapheaders]

    maps = {}
    for istep in range(len(steps) - 1):
        beg = mapheaderidx[istep] + 1
        end = mapheaderidx[istep + 1] - 1 if istep < len(mapheaders) - 1 else len(lines)
        values = [[int(x) for x in line.strip().split()] for line in lines[beg:end]]
        to_begin, from_begin, num = zip(*values)
        maps[steps[istep]] = (steps[istep + 1], RangeMap(from_begin, to_begin, num))

    return seeds, maps


def p05a(seeds, maps):
    values = []
    for seed in seeds:
        key = "seed"
        val = seed
        while key != "location":
            key, m = maps[key]
            val = m(val)
        values.append(val)

    return min(values)


def p05b_slow(seeds, maps):
    """Low coding effort, very inefficient version. Got an answer by running overnight.
[jblackburne@LAAM04 2023]$ python p05.py data/input_p05.txt
Problem 5a: 340994526
Problem 5b: 52210644
    """
    minvalue = 2**63
    seediter = iter(seeds)
    for seed_begin, nseed in zip(seediter, seediter):
        print ("Starting chunk...")
        for seed in range(seed_begin, seed_begin + nseed):
            key = "seed"
            val = seed
            while key != "location":
                key, m = maps[key]
                val = m(val)
        minvalue = min(minvalue, val)

    return minvalue


def p05b(seeds, maps):
    return p05b_slow(seeds, maps)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        seeds, maps = ingest_p05(f.readlines())

    print("Problem 5a: {}".format(p05a(seeds, maps)))
    print("Problem 5b: {}".format(p05b(seeds, maps)))
