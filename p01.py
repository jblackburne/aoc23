import sys


NUMS = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}

NUMWORDS = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def p1a(lines, numdict=NUMS):
    nums = []
    for line in lines:
        ifirsts = []
        ilasts = []
        for key in numdict:
            ifirst = line.find(key)
            ilast = line[::-1].find(key[::-1])
            if ifirst > -1:
                ifirsts.append((ifirst, ifirst + len(key)))
            if ilast > -1:
                ilast = len(line) - ilast - len(key)
                ilasts.append((ilast, ilast + len(key)))
        ifirst = min(ifirsts)
        ilast = max(ilasts)

        nums.append(10 * numdict[line[ifirst[0]:ifirst[1]]] + numdict[line[ilast[0]:ilast[1]]])

    return sum(nums)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()

    print("Problem 1a: {}".format(p1a(lines)))
    print("Problem 1b: {}".format(p1a(lines, numdict=NUMWORDS)))
