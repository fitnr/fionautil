import unittest
import fionautil.round

class RoundTestCase(unittest.TestCase):

    def testRound(self):
        ring = [(10.00011111, 10.00011111), (10.00011111, 10.00011111)]
        assert fionautil.round._round(ring[0], 1) == (10.0, 10.0)
        assert fionautil.round.round_ring(ring, 1) == [(10.0, 10.0), (10.0, 10.0)]

if __name__ == '__main__':
    unittest.main()
