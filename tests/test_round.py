import unittest
import fionautil.round


class RoundTestCase(unittest.TestCase):

    def setUp(self):
        self.polygon = {
            "type": "Polygon",
            "coordinates": [
                [
                    [100.11111, 0.0],
                    [101.0, 0.11111],
                    [101.0, 1.11111],
                    [100.11111, 1.0],
                    [100.11111, 0.0]
                ]
            ]
        }

    def testRound(self):
        ring = [(10.00011111, 10.00011111), (10.00011111, 10.00011111)]
        assert fionautil.round._round(ring[0], 1) == (10.0, 10.0)
        assert fionautil.round.round_ring(ring, 1) == [(10.0, 10.0), (10.0, 10.0)]

    def testRoundPolygon(self):
        g = fionautil.round.geometry(self.polygon, 3)
        self.assertSequenceEqual(g['coordinates'][0][0], [100.111, 0.0])

    def testRoundMultiPolygon(self):
        mp = {
            "type": "MultiPolygon",
            "coordinates": [self.polygon['coordinates'], self.polygon['coordinates']]
        }

        g = fionautil.round.geometry(mp, 3)
        self.assertSequenceEqual(g['coordinates'][0][0][0], [100.111, 0.0])

    def testRoundFeature(self):
        feat = {
            "geometry": self.polygon,
            "properties": {"foo": "bar"}
        }
        f = fionautil.round.feature(feat, 4)
        self.assertSequenceEqual(f['geometry']['coordinates'][0][0], [100.1111, 0.0])
        assert f['properties']['foo'] == 'bar'

    def testRoundGenerator(self):
        coords = enumerate(range(10))

        c = fionautil.round.round_ring(coords, 10)
        self.assertSequenceEqual(c[0], (0.0, 0.0))

        x = (float(x) + 0.555 for x in range(2))
        b = fionautil.round._round_plain(x, 2)

        self.assertSequenceEqual(b, (0.56, 1.56))


if __name__ == '__main__':
    unittest.main()
