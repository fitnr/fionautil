### fionautil

Utilities for working with geodata with [Fiona](https://pypi.python.org/pypi/Fiona/1.5.0). Some features are shorthand for [pyproj](https://pypi.python.org/pypi/pyproj) features, or add in support for projections.

## Contents

### feature

  * overlaps
  * field_contains_test (test if a feature's properties has certain key:value pairs)
  * togeojson (return a geojson-ready object)
  * shapify
  * length
  * compound

### geometry

  * endpoints (for polyline features)
  * startpoint (for polyline features)
  * endpoint (for polyline features)
  * bbox
  * azimuth (between the start and end of a polyline)
  * disjointed
  * explodepoints
  * explodesegments
  * exploderings
  * countpoints
  * countsegments

### layer

Most of these tools that mimic builtin python itertools.

  * ffilter
  * ffilterfalse
  * fmap
  * fchain
  * freduce
  * fslice
  * fzip
  * length Total length of linear features in a file's native projection or the given Proj object
  * meta (records a layers meta attribute)
  * bounds (returns a layer's bounds)
  * find (return a feature that matches a particular key=value)

### measure

  * distance (between two coordinates)
  * azimuth (between two coordinates)
  * signed_area
  * clockwise (shortcut for checking if signed_area is >= 0)
  * counterclockwise (shortcut for checking if signed_area is < 0)
  * azimuth_distance (returns both azimuth and distance between two points)

