import math

def rect(angle, length):
    '''polar to cartesian coordinates'''
    return length * math.cos(angle), length * math.sin(angle)


def polar(x, y):
    return math.hypot(x, y), math.atan2(y, x)
