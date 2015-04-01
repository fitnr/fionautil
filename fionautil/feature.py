from __future__ import print_function
from fionautil import geometry
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString


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
    return {
        'properties': feature.get('properties'),
        'geometry': geometry.shapify(feature['geometry'])
    }


def reproject(in_proj, out_proj, feature):
    feature['geometry'] = geometry.reproject(in_proj, out_proj, feature['geometry'])
    return feature


def length(feature):
    '''Returns shapely length'''
    if feature['geometry']['type'] == 'LineString':
        geom = LineString(feature['geometry']['coordinates'])

    elif feature['geometry']['type'] == 'MultiLineString':
        geom = MultiLineString(feature['geometry']['coordinates'])

    return geom.length


def compound(feature):
    '''Returns True if feature has more than one part:
    * A polygon with holes
    * A MultiPolygon or MultiLineString
    '''
    if 'Multi' in feature['geometry']['type']:
        return True

    if (feature['geometry']['type'] == 'Polygon' and
            len(feature['geometry']['coordinates']) > 1):
        return True

    return False
