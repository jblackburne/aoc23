import sys

import numpy as np
from skimage.measure import label


DELTA = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

def ingest_p18(lines):
    data = []
    for line in lines:
        direction, distance, color = line.strip().split()
        distance = int(distance)
        color = color.strip("()#")
        data.append((direction, distance, color))

    return data


def _create_grid(data):
    nodes = [(0, 0)]
    for direction, distance, _ in data:
        nodes.append((nodes[-1][0] + distance * DELTA[direction][0],
                      nodes[-1][1] + distance * DELTA[direction][1]))
    if nodes[0] != nodes[-1]:
        raise ValueError("Not a closed loop!")
    nodes = np.array(nodes)
    nodes -= nodes.min(axis=0) - 1
    nrow, ncol = nodes.max(axis=0) + 3
    grid = np.zeros((nrow, ncol), dtype=int)

    irow, icol = nodes[0]
    for direction, distance, color in data:
        for _ in range(distance):
            irow += DELTA[direction][0]
            icol += DELTA[direction][1]
            grid[irow, icol] = int(color, base=16)

    return grid


def _create_corners(data, part2=True):
    dirlist = ["R", "D", "L", "U"]

    # Set up lookahead
    data = data + [data[0]]

    irow, icol = (0, 0)
    corners = []
    for (direction, distance, color), (nextdir, _, nextcolor) in zip(data[:-1], data[1:]):
        if part2:
            direction = dirlist[int(color[-1])]
            nextdir = dirlist[int(nextcolor[-1])]
            distance = int(color[:-1], base=16)

        irow += distance * DELTA[direction][0]
        icol += distance * DELTA[direction][1]
        glyph = ("L" if (direction, nextdir) in (("D", "R"), ("L", "U")) else
                 "J" if (direction, nextdir) in (("D", "L"), ("R", "U")) else
                 "F" if (direction, nextdir) in (("U", "R"), ("L", "D")) else
                 "7" if (direction, nextdir) in (("U", "L"), ("R", "D")) else None)
        if glyph is None:
            raise ValueError("Not a 90-degree turn?!")
        corners.append((irow, icol, glyph))
    corners.sort()

    # Now group the corners into rows
    rows = []
    row = [corners[0]]
    for corner in corners[1:]:
        if corner[0] != row[0][0]:
            rows.append(row)
            row = [corner]
        else:
            row.append(corner)
    rows.append(row)

    return rows


def p18a(data):
    grid = _create_grid(data)
    labels = label(grid, background=-1)

    return (labels != labels[0, 0]).sum()


# The part 1 approach won't work for part 2 -- too much memory required
# Sigh, I guess we have to be smarter
def p18b(data, part2=True):
    corners = _create_corners(data, part2=part2)
    starts = []
    ends = []
    lastrow = None
    total_area = 0
    for corner_row in corners:
        total_width_above = sum([e - s + 1 for (s ,e) in zip (starts, ends)])
        row_width = total_width_above  # for now, but will change
        criter = iter(corner_row)
        for (irow, lcol, lglyph), (_, rcol, rglyph) in zip(criter, criter):
            if (lglyph, rglyph) == ("F", "7"):
                # Create a new span, or split an existing one
                for idx, (s, e) in enumerate(zip(starts, ends)):
                    if lcol > s and rcol < e:
                        ends.insert(idx, lcol)
                        starts.insert(idx + 1, rcol)
                        break
                else:
                    starts.append(lcol)
                    ends.append(rcol)
                    row_width += rcol - lcol + 1
            elif (lglyph, rglyph) == ("L", "J"):
                # End a span, or combine two spans
                idx_comb = []
                for idx, (s, e) in enumerate(zip(starts, ends)):
                    if lcol == s and rcol == e:
                        starts.remove(s)
                        ends.remove(e)
                        break
                    elif rcol == s:
                        idx_comb.append(idx)
                    elif lcol == e:
                        idx_comb.append(idx)
                else:
                    idx_comb.sort(key=lambda x:starts[x])
                    ends[idx_comb[0]] = ends[idx_comb[1]]
                    starts.pop(idx_comb[1])
                    ends.pop(idx_comb[1])
                    row_width += rcol - lcol - 1
            elif (lglyph, rglyph) == ("F", "J"):
                # Move a start or end to the left
                for idx, (s, e) in enumerate(zip(starts, ends)):
                    if s == rcol:
                        starts[idx] = lcol
                        row_width += rcol - lcol
                    elif e == rcol:
                        ends[idx] = lcol
            elif (lglyph, rglyph) == ("L", "7"):
                # Move a start or end to the right
                for idx, (s, e) in enumerate(zip(starts, ends)):
                    if s == lcol:
                        starts[idx] = rcol
                    elif e == lcol:
                        ends[idx] = rcol
                        row_width += rcol - lcol

        if lastrow is not None:
            total_area += (irow - lastrow - 1) * total_width_above
        total_area += row_width
        lastrow = irow

    return total_area



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p18(lines)

    print("Problem 18a: {}".format(p18a(data)))
    print("Problem 18b: {}".format(p18b(data)))
