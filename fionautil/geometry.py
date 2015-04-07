# -*- coding: utf-8 -*-
from __future__ import print_function
from . import measure


__all__ = [
    'endpoints',
    'startpoint',
    'endpoint',
    'bbox',
    'azimuth',
    'disjointed',
    'explodepoints',
    'explodesegments',
    'exploderings',
    'countpoints',
    'countsegments',
]


def endpoints(geometry):
    '''Return the first and last coordinates of a LineString or Multilinestring'''
    coords = geometry['coordinates']

    if geometry['type'] == 'MultiLineString':
        return coords[0][0], coords[-1][-1]

    elif geometry['type'] == 'LineString':
        return coords[0], coords[-1]

    raise ValueError("Improper Feature type.")


def startpoint(geometry):
    '''Return the first point in a linear geometry'''
    start, _ = endpoints(geometry)
    return start


def endpoint(geometry):
    '''Return the last point in a linear geometry'''
    _, end = endpoints(geometry)
    return end


def bbox(geometry):
    '''Return the bounds of a geometry (minx, miny, maxx, maxy)'''
    x, y = zip(*list(explodepoints(geometry)))
    return min(x), min(y), max(x), max(y)


def azimuth(geometry, projection=None, radians=False, clockwise=False):
    '''return the azimuth between the start and end a Fiona PolyLine given a feature and a Proj instance (or note that it's cartesian-ish'''

    if geometry['type'] not in ('LineString', 'MultiLineString'):
        raise ValueError("This only works with PolyLine layers, this is: {}".format(geometry['type']))

    first, last = endpoints(geometry)
    latlong = projection.is_latlong()

    if latlong:
        x0, y0 = projection(*first, inverse=True)
        x1, y1 = projection(*last, inverse=True)

    else:
        x0, y0 = first
        x1, y1 = last

    return measure.azimuth(x0, y0, x1, y1, radians=radians, clockwise=clockwise, latlong=latlong)


def disjointed(shapes):
    '''Reduce a list of shapely shapes to those that are disjoint from the others'''
    newshapes = [shapes[0]]
    for shape in shapes[1:]:
        for i, other in enumerate(newshapes):
            if shape.intersects(other):
                newshapes[i] = other.union(shape)
                break

    return newshapes


def explodepoints(geometry):
    '''Generator that returns every coordinate a geometry'''
    if geometry['type'] == 'Point':
        yield geometry['coordinates']

    else:
        for ring in exploderings(geometry):
            for point in ring:
                yield point


def explodesegments(geometry):
    '''Generator that returns every line segment of a geometry'''
    # Sure, could just use explodepoints, but isn't that a
    # bit more memory-intensive, copying all those lists of coords?
    if geometry['type'] in ('MultiLineString', 'Polygon'):
        for ring in geometry['coordinates']:
            for i, point in enumerate(ring[:-1]):
                yield point, ring[i + 1]

    elif geometry['type'] in ('LineString', 'MultiPoint'):
        for i, point in enumerate(geometry['coordinates'][:-1]):
            yield point, geometry['coordinates'][i + 1]

    elif geometry['type'] == 'MultiPolygon':
        for poly in geometry['coordinates']:
            for ring in poly:
                for i, point in enumerate(ring[:-1]):
                    yield point, ring[i + 1]

    else:
        raise ValueError("Unknown or invalid geometry type: {}".format(geometry['type']))


def exploderings(geometry):
    '''Generator that returns every ring of a geometry.
    A ring is a list of points'''
    if geometry['type'] in ('MultiLineString', 'Polygon'):
        for ring in geometry['coordinates']:
            yield ring

    elif geometry['type'] in ('LineString', 'MultiPoint'):
        yield geometry['coordinates']

    elif geometry['type'] == 'MultiPolygon':
        for poly in geometry['coordinates']:
            for ring in poly:
                yield ring
    else:
        raise ValueError("Unkown geometry type: {}".format(geometry['type']))


def countpoints(geometry):
    '''Returns the number of points in a geometry'''
    if geometry['type'] == 'Point':
        return 1

    else:
        return sum(len(ring) for ring in exploderings(geometry))


def countsegments(geometry):
    '''Not guaranteed for (multi)point layers'''
    if geometry['type'] == 'Point':
        return 0

    else:
        return sum(len(ring) - 1 for ring in exploderings(geometry))
