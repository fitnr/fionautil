import unittest
import pyproj
import fionautil.geometry
from shapely.geometry.point import Point
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon

class GeometryTestCase(unittest.TestCase):

    def setUp(self):
        self.polygon = {'type': 'Polygon', 'coordinates': [[(-122.002301, 37.529835999999996), (-122.002236, 37.529908), (-122.002167, 37.52999), (-122.00213600000001, 37.530032999999996), (-122.002088, 37.530104), (-122.001919, 37.530451), (-122.00178, 37.530736999999995), (-122.001739, 37.530865), (-122.001711, 37.530983), (-122.001694, 37.531085), (-122.001653, 37.531376), (-122.001648, 37.531425), (-122.001639, 37.53153), (-122.00163599999999, 37.531572), (-122.001634, 37.531622), (-122.001632, 37.531647), (-122.001628, 37.531724), (-122.001627, 37.531749999999995), (-122.001616, 37.531938), (-122.001611, 37.532042), (-122.001595, 37.532178), (-122.001571, 37.532319), (-122.00153, 37.532484), (-121.992616, 37.524805), (-121.992876, 37.524935), (-121.993034, 37.525014), (-121.993212, 37.5251), (-121.993746, 37.52536), (-121.99392399999999, 37.525447), (-121.99403, 37.525498999999996), (-121.994349, 37.525656), (-121.994456, 37.525709), (-121.994869, 37.525912999999996), (-121.995685, 37.526316), (-121.995711, 37.526329), (-121.99611, 37.526525), (-121.99652499999999, 37.526728999999996), (-121.996576, 37.526754), (-121.996729, 37.526829), (-121.996781, 37.526855), (-121.996846, 37.526886999999995), (-121.997044, 37.526984), (-121.99710999999999, 37.527017), (-121.997145, 37.527034), (-121.997251, 37.527086), (-121.997287, 37.527104), (-121.99733, 37.527125), (-121.99745899999999, 37.527187999999995), (-121.997503, 37.52721), (-121.99810000000001, 37.527508), (-121.998488, 37.527695), (-121.998568, 37.527733999999995), (-121.998795, 37.527848999999996), (-122.001394, 37.529249), (-122.001506, 37.529309999999995), (-122.002196, 37.529679), (-122.00236, 37.529773999999996), (-122.002301, 37.529835999999996)]]}

        self.linestring = {'type': 'LineString', 'coordinates': [(1698558.6560016416, 785359.5722958631), (1698570.6255255828, 785357.1199829046), (1698592.7188758815, 785353.618717982), (1698615.888545638, 785342.774320389), (1698632.1053597904, 785336.6905814429), (1698651.8725316962, 785330.0421180109), (1698659.045153662, 785327.3537529241), (1698688.1001785155, 785316.4641486479), (1698696.6319864516, 785313.4574198754), (1698717.936275069, 785303.1641204398), (1698733.601512783, 785295.2805483269), (1698757.090320928, 785281.0787615285), (1698773.2214488257, 785270.9157159382), (1698802.13278612, 785251.4878775944), (1698839.0495838472, 785227.758052662), (1701103.0715925542, 785570.0575142633), (1701117.0415831083, 785569.3192712615), (1701143.1992729052, 785566.1717272209), (1701168.650131336, 785560.3315072984), (1701209.706061085, 785548.4685232819), (1701250.512021864, 785532.6336759274), (1701281.5801281473, 785515.853762881), (1701310.5929042343, 785499.6991391898), (1701378.6116007813, 785459.892916804), (1701445.1270219584, 785422.3276661132), (1701482.1400952877, 785402.5158508102), (1701506.6506188242, 785391.8440056049), (1701523.390860305, 785385.4644141722), (1701559.0541053142, 785373.9359225394), (1701572.477673862, 785369.6783910012)]}

        self.epsgpoly = [(1867225.3631415186, 615357.5771661324), (1867231.2356635556, 615365.4745198288), (1867237.479480026, 615374.4758658895), (1867240.2956402097, 615379.2034383449), (1867244.6640119287, 615387.0139517855), (1867260.2170524723, 615425.2795272444), (1867273.010158651, 615456.8187370438), (1867276.8613616587, 615470.9642739793), (1867279.5459099195, 615484.0185862744), (1867281.2298689168, 615495.3130386977), (1867285.371296512, 615527.5460854613), (1867285.9004078459, 615532.9763432294), (1867286.8827223033, 615544.6150411123), (1867287.2226247364, 615549.2713711904), (1867287.4884011522, 615554.816849761), (1867287.7096603888, 615557.5881709672), (1867288.2002566787, 615566.1269034279), (1867288.3349251715, 615569.010609063), (1867289.6417699724, 615589.8566742853), (1867290.268811733, 615601.3900791614), (1867291.9249083567, 615616.458807302), (1867294.2968654872, 615632.0710232898), (1867298.2138406327, 615650.3223257487), (1868072.3540395212, 614785.6087283635), (1868049.6055425154, 614800.4009144845), (1868035.7814955255, 614809.390042857), (1868020.2022930041, 614819.1841641953), (1867973.4684487754, 614848.7886375139), (1867957.8911653375, 614858.6938429191), (1867948.6151616173, 614864.6136581865), (1867920.7006236156, 614882.4855442767), (1867911.3380669476, 614888.517779165), (1867875.1994654038, 614911.7379168055), (1867803.7977765708, 614957.6097095839), (1867801.523018313, 614959.0889994473), (1867766.6081204978, 614981.402105804), (1867730.2935749195, 615004.625704356), (1867725.8307135513, 615007.4719455142), (1867712.4421478317, 615016.0106834827), (1867707.8926967685, 615018.9693142391), (1867702.2049999998, 615022.6121230425), (1867684.8785847616, 615033.655780871), (1867679.1043068136, 615037.4109857872), (1867676.0413041625, 615039.3469008117), (1867666.7657036753, 615045.267033074), (1867663.6161057586, 615047.3153330811), (1867659.8532002757, 615049.7064320575), (1867648.5644968417, 615056.879739293), (1867644.7149993733, 615059.3832257404), (1867592.4836593368, 615093.2956794645), (1867558.5260306897, 615114.5954067486), (1867551.525267213, 615119.0363117309), (1867531.6683507564, 615132.1187283283), (1867304.4725995616, 615291.1535361662), (1867294.683327623, 615298.0812909331), (1867234.3626622162, 615340.006498295), (1867220.038663901, 615350.7809663619), (1867225.3631415186, 615357.5771661324)]

        self.multipolygon = {'type': 'MultiPolygon', 'coordinates': [[[(-156.71787267699898, 21.137419760764438), (-156.76604819764898, 21.06517681773707), (-156.8864840998058, 21.04913411712499), (-157.07113192831787, 21.105330956858555), (-157.28789752278652, 21.081250571840183), (-157.30394879695828, 21.137448432663767), (-157.2477475061229, 21.161530451508398), (-157.23169415834994, 21.233776323139818), (-157.16747148788883, 21.19364045634365), (-157.00690374246722, 21.18561063798249), (-156.95873348755612, 21.209693513430512), (-156.94268251253186, 21.161526867134565), (-156.71787267699898, 21.137419760764438)]], [[(-156.1960454124824, 20.631649407365213), (-156.27631740739284, 20.583483860915248), (-156.3967349429455, 20.567426981472988), (-156.43687923087785, 20.623621217336662), (-156.46097189319752, 20.727981087256364), (-156.49307474018514, 20.792204281510333), (-156.5251935717042, 20.776149657497466), (-156.63758660416465, 20.80826091204387), (-156.69378263402297, 20.912624010061208), (-156.65363600731771, 21.016985049562912), (-156.5974396197875, 21.041064705415824), (-156.5251916458635, 20.98487016377238), (-156.47702205254387, 20.89656513911172), (-156.3566035032919, 20.9447263610079), (-156.26026336307226, 20.928671268747912), (-156.01139245254785, 20.800225321607478), (-155.98731705257018, 20.752061631687628), (-156.0435115425545, 20.65573259996677), (-156.1318089039728, 20.62362291867985), (-156.1960454124824, 20.631649407365213)]], [[(-157.03905067093797, 20.928706972385005), (-156.91058584516276, 20.928718617694337), (-156.80620534154883, 20.84041861217258), (-156.81422569781648, 20.7922527172797), (-156.88648717839553, 20.73604940916775), (-156.96676559866026, 20.728020731638775), (-156.9908634657756, 20.792237151462064), (-156.9828263229743, 20.832377626807837), (-157.05509821197901, 20.880538425907034), (-157.03905067093797, 20.928706972385005)]]]}


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

    def test_reproject(self):
        in_proj = pyproj.Proj(init='EPSG:4269')
        out_proj = pyproj.Proj(init='epsg:26943')
        reprojected = fionautil.geometry.reproject(in_proj, out_proj, self.polygon)
        self.assertEqual(reprojected['coordinates'][0][0], self.epsgpoly[0])
        self.assertEqual(reprojected['coordinates'][0], self.epsgpoly)

    def test_shapify(self):
        ls = fionautil.geometry.shapify(self.linestring)
        assert isinstance(ls, LineString)

        pg = fionautil.geometry.shapify(self.polygon)
        assert isinstance(pg, Polygon)

        mpg = fionautil.geometry.shapify(self.multipolygon)
        assert isinstance(mpg, MultiPolygon)


if __name__ == '__main__':
    unittest.main()
