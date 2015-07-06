
def max_x(coords):
    return max((c[0] for c in coords))

def max_y(coords):
    return max((c[1] for c in coords))

def min_x(coords):
    return min((c[0] for c in coords))

def min_y(coords):
    return min((c[1] for c in coords))

def minimum(coords, dist=None):
    dist = dist or (lambda c: c[0]**2 + c[1]**2)
    return sorted(coords, key=dist).pop(0)

def maximum(coords, dist=None):
    dist = dist or (lambda c: c[0]**2 + c[1]**2)
    return sorted(coords, key=dist).pop()
