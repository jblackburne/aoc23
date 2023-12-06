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

    def eval_ranges(self, ranges):
        # First divide up our input range into a number of contiguous ranges
        # that each overlap with zero or one mapping ranges
        inranges = ranges
        for sfb, sn in zip(self.from_begin, self.num):
            inranges_mod = []
            for b, n in inranges:
                if b < sfb and sfb + sn < b + n:
                    inranges_mod.append((b, sfb - b))
                    inranges_mod.append((sfb, sn))
                    inranges_mod.append((sfb + sn, b + n - sfb - sn))
                elif b < sfb < b + n:
                    inranges_mod.append((b, sfb - b))
                    inranges_mod.append((sfb, b + n - sfb))
                elif b < sfb + sn < b + n:
                    inranges_mod.append((b, sfb + sn - b))
                    inranges_mod.append((sfb + sn, b + n - sfb - sn))
                else:
                    inranges_mod.append((b, n))
            inranges = inranges_mod
        inranges.sort()

        # Now just evaluate the input ranges and return the mapped ranges
        outranges = []
        for b, n in inranges:
            out = (b, n)  # default case if no map range
            for sfb, stb, sn in zip(self.from_begin, self.to_begin, self.num):
                if sfb <= b < sfb + sn:
                    out = (stb + b - sfb, n)
            outranges.append(out)

        return outranges


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


def p05b_fast(seeds, maps):
    """Much more coding effort because I had to write the eval_ranges()
    method. But extremely fast.
    """
    seediter = iter(seeds)
    locranges = []
    for seed_begin, nseed in zip(seediter, seediter):
        key = "seed"
        ranges = [(seed_begin, nseed)]
        while key != "location":
            key, m = maps[key]
            ranges = m.eval_ranges(ranges)
        locranges.extend(ranges)

    return min([begin for begin, num in locranges])


def p05b(seeds, maps):
    return p05b_fast(seeds, maps)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        seeds, maps = ingest_p05(f.readlines())

    print("Problem 5a: {}".format(p05a(seeds, maps)))
    print("Problem 5b: {}".format(p05b(seeds, maps)))
