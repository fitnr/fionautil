import shapely.affinity
from shapely.geometry import mapping
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon

GEOMS = {
    'LineString': LineString,
    'MultiLineString': MultiLineString,
    'MultiPoint': MultiPoint,
    'MultiPolygon': MultiPolygon,
    'Polygon': Polygon
}

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

def rotate(feature, angle, **kwargs):
    '''Rotate a feature's geometry and return the result'''
    try:
        shape = GEOMS[feature['geometry']['type']](feature['geometry']['coordinates'])
    except KeyError:
        raise KeyError("Can't rotate geometry of type {}".format(feature['geometry']['type']))

    feature['geometry'] = mapping(shapely.affinity.rotate(shape, angle, **kwargs))
    return feature
