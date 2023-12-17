import sys
import re


def ingest_p12(lines):
    data = []
    for line in lines:
        springs, seqs = line.strip().split()
        seqs = tuple([int(x) for x in seqs.split(",")])
        data.append((springs, seqs))

    return data


def _find_first_pos(spr, spos, seq):
    pattern = "[\\.\\?]+?([#\\?]{{{}}})[\\.\\?]".format(seq)
    m = re.match(pattern, spr[spos:])
    return None if m is None else m.span(1)[0] + spos


def _find_final_seq(spr, spos, seq):
    pattern = "[\\.\\?]+?([#\\?]{{{}}})[\\.\\?]+$".format(seq)
    m = re.match(pattern, spr[spos:])
    return None if m is None else m.span(1)[0] + spos


def p12a(data):
    counts = []
    for spr, seqs in data:
        count = 0
        if len(seqs) == 0:
            counts.append(count)
            continue
        spr = ".{}.".format(spr)  # pad it so the regex works
        tasks = [(0, seqs)]
        while len(tasks) > 0:
            spos, seqs = tasks.pop()
            if len(seqs) == 1:
                while spos < len(spr) - seqs[0]:
                    mpos = _find_final_seq(spr, spos, seqs[0])
                    if mpos is not None:
                        count += 1
                        spos = mpos
                    else:
                        break
            else:
                mpos = _find_first_pos(spr, spos, seqs[0])
                if mpos is not None:
                    tasks.append((mpos, seqs))
                    tasks.append((mpos + seqs[0], seqs[1:]))
        counts.append(count)

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
    print("Problem 12b: {}".format(p12b(data)))
