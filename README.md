### fionautil

Utilities for working with geodata with [Fiona](https://pypi.python.org/pypi/Fiona/1.5.0).

By default, the only prerequisite is Fiona itself.

By default, the package installs without shapely. A small number of functions, marked below, do require shapely. To use these function, install with `pip install fionautil[functionname]` or just separately install shapely.

## Contents

### drivers

  Tools for fetching the driver name, given a file suffix

  * from_file
  * From suffix

### feature

  * field_contains_test (test if a feature's properties has certain key:value pairs)
  * togeojson (return a geojson-ready object)
  * shapify (requires shapely)
  * length (requires shapely)
  * compound

### geometry

  * endpoints (for polyline features)
  * startpoint (for polyline features)
  * endpoint (for polyline features)
  * azimuth (between the start and end of a polyline)
  * disjointed
  * explodepoints
  * explodesegments
  * exploderings
  * countpoints
  * countsegments
  * roundgeometry - round all coordinates in a geometry to a given precision

### layer

Most of these tools mimic builtin python itertools.

  * ffilter
  * ffilterfalse
  * fmap
  * fchain
  * freduce
  * fslice
  * fzip
  * length Total length of linear features in a file's native projection or the given Proj object
  * meta (returns a layer's meta attribute)
  * meta_complete (returns the meta attribute with addional metadata, e.g. bounds)
  * bounds (returns a layer's bounds)
  * find (return a feature that matches a particular key=value)

### measure

  * distance (between two coordinates)
  * azimuth (between two coordinates)
  * signed_area
  * clockwise (shortcut for checking if signed_area is >= 0)
  * counterclockwise (shortcut for checking if signed_area is < 0)
  * azimuth_distance (returns both azimuth and distance between two points)
  * intersect (check if two planar line segments intersect)
  * onsegment (check if a point lines on a line segment)

### round
  * geometry - round all coordinates in a geometry to a specified precision
  * feature

### scale

  Utilities for scaling a feature or geometry by a given constant. Goes faster with Numpy installed.

  * geometry
  * scale_rings
  * scale - scales a list of coordinates
  * feature - scale the geometry of a feature
