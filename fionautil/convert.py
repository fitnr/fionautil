import math
import cmath

def rect(angle, length):
    '''polar to cartesian coordinates'''
    return length * math.cos(angle), length * math.sin(angle)


def polar(x, y):
    return math.hypot(x, y), math.atan2(y, x)


def angle_to_complex(angle):
    '''Convert radian clockwise angle to a complex vector of len 1'''
    return cmath.rect(1, -angle)
