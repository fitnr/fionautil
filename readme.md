### fionautil

Utilities for working with geodata with [Fiona](https://pypi.python.org/pypi/Fiona/1.5.0). Some features are shorthand for [pyproj](https://pypi.python.org/pypi/pyproj) features, or add in support for projections.

## Contents

* convert
  * rect (from polar)
  * polar (to rect)

* feature
  * endpoint (for polyline features)
  * startpoint (for polyline features)
  * endpoint (for polyline features)
  * azimuth (between the start and end of a polyline)
  * rotate
  * field_contains_test (test if a feature's properties has certain key:value pairs)
  * geojson_feature (return a geojson-ready object)

* geometry
  * explode (generator that yields the pairs of points from a geometry)
  * reproject (convert a geometry from one projection to another)

* measure
  * distance (between two lat, lng)
  * azimuth (between two lat, lng or two projected points)

* layer (tools that mimic basic python itertools)
  * ffilter
  * ffilterfalse
  * fmap
  * fchain
  * freduce
  * fslice
  * fzip
  * find (return a feature that matches a particular key=value)

* rotation
  * point
  * linestring
