from __future__ import print_function
from fionautil import geometry

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
    return geometry.shapify(feature['geometry'])
