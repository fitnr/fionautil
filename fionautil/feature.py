import math
from . import measure, rotation


def endpoints(feature):
    '''Return the first and last coordinates of a LineString or Multilinestring'''
    coords = feature['geometry']['coordinates']

    if feature['geometry']['type'] == 'MultiLineString':
        return coords[0][0], coords[-1][-1]

    elif feature['geometry']['type'] == 'LineString':
        return coords[0], coords[-1]

    raise ValueError("Improper Feature type.")


def startpoint(feature):
    start, _ = endpoints(feature)
    return start


def endpoint(feature):
    _, end = endpoints(feature)
    return end


def azimuth(feature, projection, radians=None):
    '''return the azimuth of a fiona LineString given a feature and a Proj instance'''

    if feature['geometry']['type'] not in ('LineString', 'MultiLineString'):
        raise ValueError("This only works with PolyLine layers, this is: {}".format(feature['geometry']['type']))

    first, last = endpoints(feature)

    x0, y0 = projection(*first, inverse=True)
    x1, y1 = projection(*last, inverse=True)

    return measure.azimuth(x0, y0, x1, y1, radians=radians)


def rotate(feature, angle=None, projected=None):
    '''rotate line feature. by default, endpoint will lie directly below start'''
    angle = angle or math.pi

    if feature['geometry']['type'] == 'LineString':
        newcoords = rotation.linestring(feature['geometry']['coordinates'], angle, projected=projected)

    elif feature['geometry']['type'] == 'MultiLineString':
        base = feature['geometry']['coordinates'][0][0]
        newcoords = []
        for line in feature['geometry']['coordinates']:
            newcoords.append(rotation.linestring(line, angle, base, projected=projected))
    else:
        raise ValueError("What? {}".format(feature))

    feature['geometry']['coordinates'] = newcoords

    return feature


def field_contains_test(field_values):
    '''Return a test function that checks if the properties of a feature '''
    def test(feature):
        for k, v in field_values.items():
            if feature['properties'].get(k) not in v:
                return False
        return True

    return test


def geojson_feature(typ, coordinates, properties=None):
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
