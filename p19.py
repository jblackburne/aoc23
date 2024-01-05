import sys
from math import prod


def ingest_p19(lines):
    lineiter = iter(lines)

    workflows = {}
    for line in lineiter:
        if len(line.strip()) == 0:
            break
        name, wf = [x.rstrip("}") for x in line.strip().split("{")]
        steps = wf.split(",")
        step_pairs = [tuple(step.split(":")) if ":" in step else ("True", step)
                      for step in steps]
        workflows[name] = tuple(step_pairs)

    ratings = []
    for line in lineiter:
        rating = line.strip("{}\n").split(",")
        ratings.append(tuple([int(r[2:]) for r in rating]))

    return workflows, ratings


def _clip(val, lo, hi):
    return min(max(val, lo), hi)


def p19a(workflows, ratings):
    total = 0
    for x, m, a, s in ratings:
        wfkey = "in"
        while wfkey not in ("A", "R"):
            wf = workflows[wfkey]
            for pred, dest in wf:
                if eval(pred):
                    wfkey = dest
                    break
        if wfkey == "A":
            total += x + m + a + s

    return total


def p19b(workflows):
    ranges = {
        "x": (1, 4001),
        "m": (1, 4001),
        "a": (1, 4001),
        "s": (1, 4001),
    }
    total_combos = 0
    tasks = [(ranges, "in")]
    while len(tasks) > 0:
        ranges, wfkey = tasks.pop(0)
        if wfkey == "R":
            continue
        if wfkey == "A":
            total_combos += prod([hi - lo for (lo, hi) in ranges.values()])
            continue
        wf = workflows[wfkey]
        for pred, dest in wf:
            if pred == "True":
                tasks.append((ranges, dest))
                break
            attr = pred[0]
            lo, hi = ranges[attr]
            op = pred[1]
            thresh = int(pred[2:])
            if op == "<":
                range_true = (lo, _clip(thresh, lo, hi))
                range_false = (_clip(thresh, lo, hi), hi)
            else:  # >
                range_true = (_clip(thresh + 1, lo, hi), hi)
                range_false = (lo, _clip(thresh + 1, lo, hi))
            if range_true[1] > range_true[0]:
                tasks.append(({**ranges, attr:range_true}, dest))
            if range_false[1] > range_false[0]:
                ranges[attr] = range_false
            else:
                break

    return total_combos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    workflows, ratings = ingest_p19(lines)

    print("Problem 19a: {}".format(p19a(workflows, ratings)))
    print("Problem 19b: {}".format(p19b(workflows)))
