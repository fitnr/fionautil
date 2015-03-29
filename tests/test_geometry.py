import unittest
import fionautil.geometry

class GeometryTestCase(unittest.TestCase):

    def setUp(self):
        self.polygon = {'type': 'Polygon', 'coordinates': [[(-122.002301, 37.529835999999996), (-122.002236, 37.529908), (-122.002167, 37.52999), (-122.00213600000001, 37.530032999999996), (-122.002088, 37.530104), (-122.001919, 37.530451), (-122.00178, 37.530736999999995), (-122.001739, 37.530865), (-122.001711, 37.530983), (-122.001694, 37.531085), (-122.001653, 37.531376), (-122.001648, 37.531425), (-122.001639, 37.53153), (-122.00163599999999, 37.531572), (-122.001634, 37.531622), (-122.001632, 37.531647), (-122.001628, 37.531724), (-122.001627, 37.531749999999995), (-122.001616, 37.531938), (-122.001611, 37.532042), (-122.001595, 37.532178), (-122.001571, 37.532319), (-122.00153, 37.532484), (-121.992616, 37.524805), (-121.992876, 37.524935), (-121.993034, 37.525014), (-121.993212, 37.5251), (-121.993746, 37.52536), (-121.99392399999999, 37.525447), (-121.99403, 37.525498999999996), (-121.994349, 37.525656), (-121.994456, 37.525709), (-121.994869, 37.525912999999996), (-121.995685, 37.526316), (-121.995711, 37.526329), (-121.99611, 37.526525), (-121.99652499999999, 37.526728999999996), (-121.996576, 37.526754), (-121.996729, 37.526829), (-121.996781, 37.526855), (-121.996846, 37.526886999999995), (-121.997044, 37.526984), (-121.99710999999999, 37.527017), (-121.997145, 37.527034), (-121.997251, 37.527086), (-121.997287, 37.527104), (-121.99733, 37.527125), (-121.99745899999999, 37.527187999999995), (-121.997503, 37.52721), (-121.99810000000001, 37.527508), (-121.998488, 37.527695), (-121.998568, 37.527733999999995), (-121.998795, 37.527848999999996), (-122.001394, 37.529249), (-122.001506, 37.529309999999995), (-122.002196, 37.529679), (-122.00236, 37.529773999999996), (-122.002301, 37.529835999999996)]]}

        self.linestring = {'type': 'LineString', 'coordinates': [(1698558.6560016416, 785359.5722958631), (1698570.6255255828, 785357.1199829046), (1698592.7188758815, 785353.618717982), (1698615.888545638, 785342.774320389), (1698632.1053597904, 785336.6905814429), (1698651.8725316962, 785330.0421180109), (1698659.045153662, 785327.3537529241), (1698688.1001785155, 785316.4641486479), (1698696.6319864516, 785313.4574198754), (1698717.936275069, 785303.1641204398), (1698733.601512783, 785295.2805483269), (1698757.090320928, 785281.0787615285), (1698773.2214488257, 785270.9157159382), (1698802.13278612, 785251.4878775944), (1698839.0495838472, 785227.758052662), (1701103.0715925542, 785570.0575142633), (1701117.0415831083, 785569.3192712615), (1701143.1992729052, 785566.1717272209), (1701168.650131336, 785560.3315072984), (1701209.706061085, 785548.4685232819), (1701250.512021864, 785532.6336759274), (1701281.5801281473, 785515.853762881), (1701310.5929042343, 785499.6991391898), (1701378.6116007813, 785459.892916804), (1701445.1270219584, 785422.3276661132), (1701482.1400952877, 785402.5158508102), (1701506.6506188242, 785391.8440056049), (1701523.390860305, 785385.4644141722), (1701559.0541053142, 785373.9359225394), (1701572.477673862, 785369.6783910012)]}


    def test_explodepoints_polygon(self):
        explode = fionautil.geometry.explodepoints(self.polygon)
        self.assertEqual(next(explode), self.polygon['coordinates'][0][0])
        self.assertEqual(next(explode), self.polygon['coordinates'][0][1])

    def test_explodepoints_linestring(self):
        explode = fionautil.geometry.explodepoints(self.linestring)
        self.assertEqual(next(explode), self.linestring['coordinates'][0])
        self.assertEqual(next(explode), self.linestring['coordinates'][1])

    def test_exploderings_polygon(self):
        explode = fionautil.geometry.exploderings(self.polygon)
        self.assertEqual(next(explode), self.polygon['coordinates'][0])

    def test_exploderings_linestring(self):
        explode = fionautil.geometry.exploderings(self.linestring)
        self.assertEqual(next(explode), self.linestring['coordinates'])
        self.assertRaises(StopIteration, next, explode)

    def test_endpoints(self):
        self.assertRaises(ValueError, fionautil.geometry.endpoints, self.polygon)

        self.assertEqual(fionautil.geometry.endpoints(self.linestring), (self.linestring['coordinates'][0], self.linestring['coordinates'][-1]))



if __name__ == '__main__':
    unittest.main()
