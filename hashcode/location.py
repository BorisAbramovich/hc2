from collections import namedtuple

from math import sqrt, ceil

Location = namedtuple('Location', 'row col')


def dist(loc1: Location, loc2: Location):
    return ceil(sqrt(
        (loc1.row - loc2.row) ** 2 +
        (loc1.col - loc2.col) ** 2
    ))