import sys
from collections import Counter

import numpy as np


CARD_VALUE = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

CARD_NAME = {v: k for k, v in CARD_VALUE.items()}

# Hand types ranked
FIVE_KIND = 6
FOUR_KIND = 5
FULL_HOUSE = 4
THREE_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0


def ingest_p07(lines):
    data = []
    for line in lines:
        handstr, bidstr = line.strip().split()
        hand = tuple([CARD_VALUE[x] for x in handstr])
        bid = int(bidstr)
        data.append((hand, bid))

    return data


def hand_key(hand, jokerval=None):
    counter = Counter(hand)
    nuniq = len(counter)
    maxsame = max(counter.values())
    njokers = counter[jokerval]

    # Figure out the type of the hand assuming no jokers
    if nuniq == 1:
        hand_type = FIVE_KIND
    elif nuniq == 2:
        hand_type = FOUR_KIND if maxsame == 4 else FULL_HOUSE
    elif nuniq == 3:
        hand_type = THREE_KIND if maxsame == 3 else TWO_PAIR
    elif nuniq == 4:
        hand_type = ONE_PAIR
    else:  # five unique entries
        hand_type = HIGH_CARD

    if jokerval is not None:
        # Upgrade hands if they have jokers
        if hand_type == FOUR_KIND and njokers > 0:
            hand_type = FIVE_KIND
        elif hand_type == FULL_HOUSE and njokers > 0:
            hand_type = FIVE_KIND
        elif hand_type == THREE_KIND and njokers > 0:
            hand_type = FOUR_KIND
        elif hand_type == TWO_PAIR:
            if njokers == 1:
                hand_type = FULL_HOUSE
            elif njokers == 2:
                hand_type = FOUR_KIND
        elif hand_type == ONE_PAIR and njokers > 0:
            hand_type = THREE_KIND
        elif hand_type == HIGH_CARD and njokers > 0:
            hand_type = ONE_PAIR

    return (hand_type,) + hand


def p07a(data):
    hands, bids = zip(*data)

    keys = [hand_key(x) for x in hands]
    idx = np.lexsort(tuple(zip(*keys))[::-1])

    return np.dot(np.arange(1, len(hands) + 1), np.array(bids)[idx])


def p07b(data):
    hands, bids = zip(*data)

    # Whoops, Js are jokers now
    jackval = CARD_VALUE["J"]
    jokerval = 1
    hands = [tuple([c if c != jackval else jokerval for c in hand])
             for hand in hands]

    keys = [hand_key(x, jokerval=jokerval) for x in hands]
    idx = np.lexsort(tuple(zip(*keys))[::-1])

    return np.dot(np.arange(1, len(hands) + 1), np.array(bids)[idx])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        data = ingest_p07(f.readlines())

    print("Problem 7a: {}".format(p07a(data)))
    print("Problem 7b: {}".format(p07b(data)))
