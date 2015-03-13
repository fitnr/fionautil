import cmath

def angle_to_complex(angle):
    '''Convert radian clockwise angle to a complex vector of len 1'''
    return cmath.rect(1, -angle)

def round_even(n, ndigits=0):
    return round(round(round(n * 10 ** ndigits, ndigits) / 2) * 2 / 10 ** ndigits, ndigits)
