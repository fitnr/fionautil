from __future__ import print_function
import sys
from itertools import chain
import pyproj
from shapely.geometry.point import Point
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from . import measure
from .coordinates import transform_multi, transform_line


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
    'reproject',
    'countpoints',
    'countsegments',
    'shapify',
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
    start, _ = endpoints(geometry)
    return start


def endpoint(geometry):
    _, end = endpoints(geometry)
    return end


def bbox(geometry):
    x, y = zip(*list(explodepoints(geometry)))
    return min(x), min(y), max(x), max(y)


def azimuth(geometry, projection=None, radians=False, clockwise=False):
    '''return the azimuth of a fiona LineString given a feature and a Proj instance (or note that it's cartesian-ish'''

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


def reproject(in_proj, out_proj, geometry):
    '''Transform a Fiona/GeoJSON geometry into another projection'''
    if geometry['type'] == 'MultiPolygon':
        coords = [transform_multi(in_proj, out_proj, c) for c in geometry['coordinates']]

    if geometry['type'] in ('MultiLineString', 'Polygon'):
        coords = transform_multi(in_proj, out_proj, geometry['coordinates'])

    elif geometry['type'] in ('LineString', 'MultiPoint'):
        coords = transform_line(in_proj, out_proj, geometry['coordinates'])

    elif geometry['type'] == 'Point':
        coords = pyproj.transform(in_proj, out_proj, *geometry['coordinates'])

    else:
        raise ValueError("Unkown geometry type: {}".format(geometry['type']))

    return coords


def countpoints(geometry):
    if geometry['type'] == 'Point':
        length = 1

    elif geometry['type'] in ('Linestring', 'MultiPoint'):
        length = len(geometry['coordinates'])

    if geometry['type'] in ('MultiLinestring', 'Polygon'):
        length = len(list(chain(*geometry['coordinates'])))

    elif geometry['type'] in ('MultiPolygon'):
        length = len(list(chain(*chain(*geometry['coordinates']))))

    else:
        raise ValueError("Unkown geometry type: {}".format(geometry['type']))

    return length


def countsegments(geometry):
    '''Not guaranteed for (multi)point layers'''
    return countpoints(geometry) - 1

def _multipolygonize(coordinates):
    return MultiPolygon([_polygonize(x) for x in coordinates])

def _polygonize(coordinates):
    return Polygon(coordinates[0], coordinates[1:])

GEOMS = {
    'Point': Point,
    'MultiPoint': MultiPoint,
    'LineString': LineString,
    'MultiLineString': MultiLineString,
    'Polygon': _polygonize,
    'MultiPolygon': _multipolygonize
}

def shapify(geometry):
    try:
        return GEOMS[geometry['type']](geometry['coordinates'])

    except (IndexError, ValueError) as e:
        print('Error Shapifying', file=sys.stderr)
        print(geometry, file=sys.stderr)
        raise e

    except KeyError:
        raise ValueError("Can't shapify that kind of feature.")
