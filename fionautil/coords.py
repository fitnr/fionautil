
def max_x(coords):
    return max((c[0] for c in coords))

def max_y(coords):
    return max((c[1] for c in coords))

def min_x(coords):
    return min((c[0] for c in coords))

def min_y(coords):
    return min((c[1] for c in coords))

def segmentize(ring):
    for i, point in enumerate(ring[:-1]):
        yield point, ring[i + 1]

def bounds(ring):
    '''Return minimum bounding rectangle for a ring'''
    return min_x(ring), min_y(ring), max_x(ring), max_y(ring)

def roundring(ring, precision=None):
    precision = 5 if precision is None else precision

    return [(round(x, precision), round(y, precision)) for x, y in ring]

def roundpolyring(polyring, precision=None):
    return [roundring(ring, precision) for ring in polyring]

