from __future__ import print_function
import sys
from shapely.geometry.point import Point
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon

GEOMS = {
    'Point': Point,
    'LineString': LineString,
    'MultiLineString': MultiLineString,
    'MultiPoint': MultiPoint,
    'MultiPolygon': MultiPolygon,
    'Polygon': Polygon
}

MULTIS = {
    'MultiLineString': LineString,
    'MultiPoint': Point,
    'MultiPolygon': Polygon
}

def field_contains_test(field_values):
    '''Return a test function that checks if the properties of a feature '''
    def test(feature):
        for k, v in field_values.items():
            if feature['properties'].get(k) not in v:
                return False
        return True

    return test


def overlaps(feature, bbox):
    '''Returns true if feature overlaps bbox (xmin, ymin, xmax, ymax)'''
    xm0, ym0, xM0, yM0 = bbox
    xm1, ym1, xM1, yM1 = geometry.bbox(feature['geometry'])
    if yM1 < ym0 or yM0 < ym1:
        return False

    if xM1 < xm0 or xM0 < xm1:
        return False

    return True

def togeojson(typ, coordinates, properties=None):
    '''Return a GeoJSON-ready object given a properties dict, a type and coordinates.'''
    properties = properties or {}

    return {
        'type': 'Feature',
        'properties': properties,
        'geometry': {
            'type': typ,
            'coordinates': coordinates,
        }
    }


def shapify(feature):
    typ = feature['geometry']['type']
    try:
        if typ == 'MultiPolygon':
            # TODO is this right?
            coords = [Polygon(x[0]) for x in feature['geometry']['coordinates']]
        else:
            coords = feature['geometry']['coordinates']

    except ValueError as e:
        print('Error Shapifying', file=sys.stderr)
        print(feature, file=sys.stderr)
        raise e

    return GEOMS[typ](coords)
