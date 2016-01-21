try:
    import numpy as np
except ImportError:
    pass


def _round(pt, precision):
    try:
        return round(pt[0], precision), round(pt[1], precision)

    except TypeError:
        pt = list(pt)
        return round(pt[0], precision), round(pt[1], precision)


def round_ring(ring, precision):
    return [_round(pt, precision) for pt in ring]

def geometry(geom, precision):
    g = dict(geom.items())

    try:
        c = np.array(geom['coordinates'])
        g['coordinates'] = np.round(c, precision)

    except (AttributeError, KeyError, NameError):

        if geom['type'] == 'Point':
            g['coordinates'] = _round(geom['coordinates'][:], precision)

        elif geom['type'] in ('MultiPoint', 'LineString'):
            g['coordinates'] = round_ring(geom['coordinates'][:], precision)

        elif geom['type'] in ('MultiLineString', 'Polygon'):
            g['coordinates'] = [round_ring(r, precision) for r in geom['coordinates'][:]]

        elif geom['type'] == 'MultiPolygon':
            g['coordinates'] = [[round_ring(r, precision) for r in rings] for rings in geom['coordinates'][:]]

        elif geom['type'] == 'GeometryCollection':
            g['geometries'] = [geometry(g, precision) for g in geom['geometries']]

    return g


def feature(feat, precision):
    feat['geometry'] = geometry(feat['geometry'], precision)
    return feat
