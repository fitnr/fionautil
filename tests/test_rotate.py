import unittest
import cmath
import math
import fionautil

def angle_to_complex(angle):
    '''Convert radian clockwise angle to a complex vector of len 1'''
    return cmath.rect(1, -angle)

class RotateTest(unittest.TestCase):

    def test_azimuth(self):
        assert fionautil.measure.azimuth(0, 45, 0, 46) == 0
        self.assertAlmostEqual(fionautil.measure.azimuth(-0, 0, -0.0001, 0), math.pi / -2)
        self.assertAlmostEqual(fionautil.measure.azimuth(-74, 0, -74.000001, 0, radians=0), -90)

        assert fionautil.measure.azimuth(0, 0, 0, -1, radians=0, projected=1) == 180
        assert fionautil.measure.azimuth(0, 0, 0, 1, radians=0, projected=1) == 0
        assert fionautil.measure.azimuth(0, 0, 1, 0, radians=0, projected=1) == 90
        assert fionautil.measure.azimuth(0, 0, -1, 0, radians=0, projected=1) == 270

    def test_rotatepoint(self):
        a = fionautil.rotation.point(math.pi, 0, 0, 1, 1)
        self.assertAlmostEqual(a[0], -1.)
        self.assertAlmostEqual(a[1], -1.)

        self.assertAlmostEqual(angle_to_complex(0), complex(1, 0))
        self.assertAlmostEqual(angle_to_complex(math.pi / 2), complex(0, -1))
        self.assertAlmostEqual(angle_to_complex(math.pi), complex(-1, 0))
        self.assertAlmostEqual(angle_to_complex(3 * math.pi / 2), complex(0, 1))

        # print fionautil.rotation.point(math.pi, 0, 0, 1, 0)
        self.assertAlmostEqual(complex(*fionautil.rotation.cpoint(0, 0, 0, 1, 0)), complex(1, 0))
        self.assertAlmostEqual(complex(*fionautil.rotation.cpoint(math.pi/2, 0, 0, 1, 0)), complex(0, -1))
        self.assertAlmostEqual(complex(*fionautil.rotation.cpoint(math.pi / 2, 1, 1, 2, 1)), complex(1, 0))

        self.assertAlmostEqual(complex(*fionautil.rotation.point(math.pi/2, 0, 0, 1, 0)), complex(0, -1))

if __name__ == '__main__':
    unittest.main()
