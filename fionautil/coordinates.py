import pyproj

def flip(x, y):
    return y, x

def transform_line(in_proj, out_proj, ring):
    xs, ys = pyproj.transform(in_proj, out_proj, *zip(*ring))  # pylint: disable=W0632
    return zip(xs, ys)


def transform_multi(in_proj, out_proj, coordinates):
    return [transform_line(in_proj, out_proj, ring) for ring in coordinates]

