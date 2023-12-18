import sys
import re


def ingest_p12(lines):
    data = []
    for line in lines:
        springs, seqs = line.strip().split()
        seqs = tuple([int(x) for x in seqs.split(",")])
        data.append((springs, seqs))

    return data


def p12a(data):
    counts = []
    for spr, seqs in data[9:10]:
        count = 0
        if len(seqs) == 0:
            counts.append(count)
            continue
        spr = spr.strip(".")
        tasks = [(0, seqs)]
        while len(tasks) > 0:
            spos, seqs = tasks.pop()
            print(spr, spos, seqs)

            # End condition
            if len(seqs) == 0:
                count += int(not any(c == "#" for c in spr[spos:]))
                print("++")
                continue

            # Early check for not enough string remaining
            min_needed = sum(seqs) + len(seqs) - 1
            if spos > len(spr) - min_needed:
                continue

            # Try to match this sequence right here
            pattern = "[#\\?]{{{}}}([\\.\\?]|$)".format(seqs[0])
            m = re.match(pattern, spr[spos:])
            sp = spos + 1
            while sp < len(spr) and spr[sp - 1] == "#": sp += 1
            while sp < len(spr) and spr[sp] == ".": sp += 1
            tasks.append((sp, seqs))
            if m is not None:
                sp = spos + seqs[0] + 1
                while sp < len(spr) and spr[sp] == ".": sp += 1
                tasks.append((sp, seqs[1:]))

        counts.append(count)
        print(count)

    return sum(counts)


def p12b(data):
    # Unfold the data, then just feed it through part a
    # DOH! This is too slow
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
    #print("Problem 12b: {}".format(p12b(data)))
