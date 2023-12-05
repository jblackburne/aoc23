import sys


def ingest_p02(lines):
    data = []
    for line in lines:
        gamestr, drawsstr = line.strip().split(":")
        gameID = int(gamestr[4:])
        linedata = [[chunk.strip().split(" ") for chunk in draw.split(",")]
                    for draw in drawsstr.split(";")]
        linedicts = [{color: int(num) for (num, color) in x} for x in linedata]

        data.append((gameID, linedicts))

    return data


def p02a(data, maxrgb):
    """Returns the sum of the game IDs of games that are possible given maxrgb.
    """
    maxred, maxgreen, maxblue = maxrgb
    validGames = []
    for gameID, gamedicts in data:
        gamered = max([d.get("red", 0) for d in gamedicts])
        gamegreen = max([d.get("green", 0) for d in gamedicts])
        gameblue = max([d.get("blue", 0) for d in gamedicts])
        if gamered <= maxred and gamegreen <= maxgreen and gameblue <= maxblue:
            validGames.append(gameID)

    return sum(validGames)


def p02b(data):
    """Calculates the minimum number of cubes that would make each game
    possible. Returns the sum of the products of those 3-vectors.
    """
    powers = []
    for gameID, gamedicts in data:
        gamered = max([d.get("red", 0) for d in gamedicts])
        gamegreen = max([d.get("green", 0) for d in gamedicts])
        gameblue = max([d.get("blue", 0) for d in gamedicts])
        powers.append(gamered * gamegreen * gameblue)

    return sum(powers)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        data = ingest_p02(f.readlines())

    print("Problem 2a: {}".format(p02a(data, (12, 13, 14))))
    print("Problem 2b: {}".format(p02b(data)))
