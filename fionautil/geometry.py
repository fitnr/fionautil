# -*- coding: utf-8 -*-
# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

from . import measure
from .round import geometry as roundgeometry

__all__ = [
    'endpoints',
    'startpoint',
    'endpoint',
    'azimuth',
    'disjointed',
    'explodepoints',
    'explodesegments',
    'exploderings',
    'countpoints',
    'countsegments',
    'roundgeometry'
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


def azimuth(geometry, crs=None, radians=None, clockwise=None, longlat=None):
    '''
    Get the azimuth between the start and end points of a polyline geometry.

    Args:
        geometry (dict): A geojson-like geometry object
        crs (dict): A fiona-style mapping
        radians (bool): Output in radians
        clockwise (bool): Use clockwise orientation.
        longlat (bool): geometry's coordinates are in long-lat form.

    Returns:
        (float) The angle (from north) described when one is standing at
                the start of the feature and pointing to the end.
    '''

    if geometry['type'] not in ('LineString', 'MultiLineString'):
        raise ValueError("This only works with PolyLine layers, this is a {type}".format(**geometry))

    crs = '' or crs
    if longlat is None and 'proj' in crs:
        longlat = crs['proj'] == 'longlat'

    first, last = endpoints(geometry)

    points = first + last

    return measure.azimuth(*points, radians=radians, clockwise=clockwise, longlat=longlat)


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

    elif geometry['type'] == 'GeometryCollection':
        for g in geometry['geometries']:
            for i, j in explodesegments(g):
                yield i, j

    else:
        raise ValueError("Unknown or invalid geometry type: {type}".format(**geometry))


def exploderings(geometry):
    '''Generator that returns every ring of a geometry (a ring is a list of points).'''
    if geometry['type'] in ('MultiLineString', 'Polygon'):
        for ring in geometry['coordinates']:
            yield ring

    elif geometry['type'] in ('LineString', 'MultiPoint'):
        yield geometry['coordinates']

    elif geometry['type'] == 'MultiPolygon':
        for poly in geometry['coordinates']:
            for ring in poly:
                yield ring

    elif geometry['type'] == 'GeometryCollection':
        for g in geometry['geometries']:
            for ring in exploderings(g):
                yield ring

    else:
        raise ValueError("Unknown or invalid geometry type: {type}".format(**geometry))


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
