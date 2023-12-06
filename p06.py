import sys
import numpy as np


def ingest_p06(lines):
    times = [int(x) for x in lines[0].strip().split()[1:]]
    distances = [int(x) for x in lines[1].strip().split()[1:]]

    return times, distances


def find_roots(time, dist):
    """Solve the quadratic equation -t**2 + T*t - d - 1 = 0 for t with
    T=time and d=dist.
    """
    # (-b +- sqrt(b**2 - 4*a*c)) / (2*a)
    a = -1
    b = time
    c = -dist - 1
    discrim = b**2 - 4 * a * c
    if discrim < 0:
        raise ValueError("Negative discriminant!?")

    soln = sorted([(-b + s * np.sqrt(discrim)) / (2 * a) for s in [-1, 1]])
    soln0 = int(np.ceil(soln[0]))
    soln1 = int(np.floor(soln[1]))

    # Check
    eqn = lambda t: -t**2 + time * t - dist
    if (eqn(soln0) <= 0 or
        eqn(soln0 - 1) > 0 or
        eqn(soln1) <= 0 or
        eqn(soln1 + 1) > 0):
        raise RuntimeError("You messed up")

    return soln0, soln1


def p06a(times, distances):
    ways = []
    for t, d in zip(times, distances):
        roots = find_roots(t, d)
        ways.append(roots[1] - roots[0] + 1)

    return np.prod(ways)


def p06b(times, distances):
    t = int("".join([str(x) for x in times]))
    d = int("".join([str(x) for x in distances]))
    roots = find_roots(t, d)

    return roots[1] - roots[0] + 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        seeds, maps = ingest_p06(f.readlines())

    print("Problem 6a: {}".format(p06a(seeds, maps)))
    print("Problem 6b: {}".format(p06b(seeds, maps)))
