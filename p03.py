import sys
import numpy as np
from skimage.measure import label
from scipy.ndimage import binary_dilation


def ingest_p03(lines):
    chars = []
    for line in lines:
        chars.append(list(line.strip().encode()))

    return np.array(chars, dtype=np.uint8)


def p03a(data):
    """Identify numbers in the array that are next to non-dot
    symbols. Evaluate them and return their sum.
    """
    numericmask = (data >= ord('0')) & (data <= ord('9'))
    symbolmask = (data != ord('.')) & np.logical_not(numericmask)

    numeric_regions = label(numericmask)
    nregions = numeric_regions.max() + 1
    region_values = np.array([int(bytes(data[numeric_regions == val]))
                              for val in range(1, nregions)])

    nsymbols = symbolmask.sum()
    number_is_partnum = np.array([label(symbolmask | (numeric_regions == val)).max() == nsymbols
                                  for val in range(1, nregions)])

    return region_values[number_is_partnum].sum()


def p03b(data):
    """Identify parts labeled with * that are next to exactly two part
    numbers. Return the sum of the products of those number pairs.
    """
    numericmask = (data >= ord('0')) & (data <= ord('9'))
    numeric_regions = label(numericmask)
    nregions = numeric_regions.max() + 1
    region_values = np.array([int(bytes(data[numeric_regions == val]))
                              for val in range(1, nregions)])

    starmask = data == ord('*')
    nstars = starmask.sum()
    star_regions = label(starmask)
    structure = np.ones((3, 3), dtype=bool)
    answer = 0
    for val in range(1, nstars + 1):
        fatstar = binary_dilation(star_regions == val, structure=structure)
        junk = np.unique(fatstar * numeric_regions)
        junk = junk[junk != 0]
        if junk.size == 2:
            answer += region_values[junk[0] - 1] * region_values[junk[1] - 1]

    return answer


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        data = ingest_p03(f.readlines())

    print("Problem 3a: {}".format(p03a(data)))
    print("Problem 3b: {}".format(p03b(data)))
