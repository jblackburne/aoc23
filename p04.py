import sys


def ingest_p04(lines):
    data = []
    for line in lines:
        label, cardinfo = line.strip().split(":")
        cardID = int(label.split()[1])
        winners, dealt = cardinfo.split("|")
        winners = tuple([int(x) for x in winners.split()])
        dealt = tuple([int(x) for x in dealt.split()])

        data.append((cardID, winners, dealt))

    return data


def p04a(data):
    score = 0
    for cardID, winners, dealt in data:
        winnersdealt = set(winners).intersection(set(dealt))
        nwin = len(winnersdealt)
        if nwin > 0:
            score += 2**(nwin - 1)

    return score


def p04b(data):
    ncards = len(data)
    ncopies = [1 for _ in range(ncards)]
    for cardID, winners, dealt in data:
        winnersdealt = set(winners).intersection(set(dealt))
        nwin = len(winnersdealt)
        for i in range(nwin):
            ncopies[cardID + i] += ncopies[cardID - 1]

    return sum(ncopies)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        data = ingest_p04(f.readlines())

    print("Problem 4a: {}".format(p04a(data)))
    print("Problem 4b: {}".format(p04b(data)))
