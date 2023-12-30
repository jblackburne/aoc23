import sys
from collections import OrderedDict


def ingest_p15(lines):
    data = []
    for line in lines:
        data.extend(line.strip().split(","))

    return data


class HASHMAP:
    def __init__(self):
        self.boxes = [OrderedDict() for _ in range(256)]

    @staticmethod
    def hash(s):
        val = 0
        for c in s:
            val += ord(c)
            val *= 17
            val %= 256
        return val

    def operate(self, chunk):
        label = chunk.rstrip("-=0123456789")
        ibox = self.hash(label)
        if chunk[-1] == "-":
            # Remove any items with this label from this box
            try:
                self.boxes[ibox].pop(label)
            except KeyError:
                pass
        elif chunk[-2] == "=":
            # Add a lens (or replace existing)
            self.boxes[ibox][label] = int(chunk[-1])

    def focusing_power(self):
        total = 0
        for ibox, box in enumerate(self.boxes, start=1):
            for ilens, focal_length in enumerate(box.values(), start=1):
                total += ibox * ilens * focal_length
        return total


def p15a(data):
    sums = []
    for chunk in data:
        sums.append(HASHMAP.hash(chunk))

    return sum(sums)


def p15b(data):
    hashmap = HASHMAP()
    for chunk in data:
        hashmap.operate(chunk)
    return hashmap.focusing_power()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p15(lines)

    print("Problem 15a: {}".format(p15a(data)))
    print("Problem 15b: {}".format(p15b(data)))
