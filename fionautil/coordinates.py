import pyproj


def flip(x, y):
    return y, x


def reproject_line(in_proj, out_proj, ring):
    xs, ys = pyproj.transform(in_proj, out_proj, *zip(*ring))  # pylint: disable=W0632
    return zip(xs, ys)


def reproject_multi(in_proj, out_proj, coordinates):
    return [reproject_line(in_proj, out_proj, ring) for ring in coordinates]


def transform(function, coordinates, each=None):
    '''Apply a function to each tuple in a coordinates.
    If each=True, the function is applied to each value in the coordinates'''
    if each:
        return [(function(x), function(y)) for x, y in coordinates]
    else:
        return [function(point) for point in coordinates]
