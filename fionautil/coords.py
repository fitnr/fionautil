# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

from .round import round_ring as roundring


def max_x(coords):
    return max((c[0] for c in coords))


def max_y(coords):
    return max((c[1] for c in coords))


def min_x(coords):
    return min((c[0] for c in coords))


def min_y(coords):
    return min((c[1] for c in coords))


def segmentize(ring):
    for i, point in enumerate(ring[:-1]):
        yield point, ring[i + 1]


def bounds(ring):
    '''Return minimum bounding rectangle for a ring'''
    return min_x(ring), min_y(ring), max_x(ring), max_y(ring)


def roundpolyring(polyring, precision=None):
    return [roundring(ring, precision) for ring in polyring]


def centerbounds(bounds):
    '''Returns the center of a bounding box.'''
    return (bounds[2] - bounds[0]) / 2, (bounds[3] - bounds[1]) / 2


def cornerbounds(bounds):
    '''Returns the four corners of a bounding box'''
    return (bounds[0], bounds[1]), (bounds[0], bounds[3]), (bounds[2], bounds[3]), (bounds[2], bounds[1])
