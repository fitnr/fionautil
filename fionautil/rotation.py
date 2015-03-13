import math
from .wgs84 import WGS84
from . import measure, util


def point(angle, cx, cy, x, y, **kwargs):
    """rotate x, y 'angle' radians about cx, cy"""
    if kwargs.get('radians', True):
        angle = -angle
    else:
        angle = math.radians(-angle)

    sin = math.sin(angle)
    cos = math.cos(angle)

    dx, dy = x - cx, y - cy

    x = dx * cos - dy * sin
    y = dx * sin + dy * cos

    return x + cy, y + cy


def linestring(coordinates, angle, base=None, projected=None):
    '''rotate WGS84 line coordinates about base'''

    if base:
        x, y = base  # pylint: disable=W0633
    else:
        x, y = coordinates[0]

    outcoords = []

    for pt in coordinates:
        if projected:
            theta = measure.azimuth(x, y, *pt, radians=True, projected=projected)
            x_, y_ = point(angle - theta, x, y, *pt)
        else:
            theta, _, dist = WGS84.inv(x, y, *pt, radians=False)
            x_, y_, _ = WGS84.fwd(x, y, angle - theta, dist, radians=False)

        outcoords.append((x_, y_))

    return outcoords


def cpoint(angle, cx, cy, x, y, **kwargs):
    """rotate x, y 'angle' radians about cx, cy *using complex math*"""
    if kwargs.get('radians', True):
        rotation = util.angle_to_complex(angle)
    else:
        rotation = util.angle_to_complex(math.radians(angle))

    new = complex(x - cx, y - cy) * rotation

    return cx + new.real, cy + new.imag
