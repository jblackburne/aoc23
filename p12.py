import sys
import re
from functools import lru_cache


def ingest_p12(lines):
    data = []
    for line in lines:
        springs, seqs = line.strip().split()
        seqs = tuple([int(x) for x in seqs.split(",")])
        data.append((springs, seqs))

    return data


@lru_cache(maxsize=None)
def _dfs(spr, spos, seqs):
    # End condition
    if len(seqs) == 0:
        return int(not any(c == "#" for c in spr[spos:]))

    # Early check for not enough string remaining
    min_needed = sum(seqs) + len(seqs) - 1
    if spos > len(spr) - min_needed:
        return 0

    # Try to match this sequence right here
    pattern = "[#\\?]{{{}}}([\\.\\?]|$)".format(seqs[0])
    m = re.match(pattern, spr[spos:])
    ret = 0
    if spr[spos] == "?":
        sp = spos + 1
        while sp < len(spr) and spr[sp] == ".": sp += 1
        ret += _dfs(spr, sp, seqs)
    if m is not None:
        sp = spos + seqs[0] + 1
        while sp < len(spr) and spr[sp] == ".": sp += 1
        ret += _dfs(spr, sp, seqs[1:])

    return ret


def p12a(data):
    counts = []
    for spr, seqs in data:
        count = 0
        if len(seqs) == 0:
            counts.append(count)
            continue
        spr = spr.strip(".")
        count = _dfs(spr, 0, seqs)

        counts.append(count)

    return sum(counts)


def p12b(data):
    # Unfold the data, then just feed it through part a
    data = [("?".join([spr] * 5), seqs * 5) for (spr, seqs) in data]
    return p12a(data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p12(lines)

    print("Problem 12a: {}".format(p12a(data)))
    print("Problem 12b: {}".format(p12b(data)))
