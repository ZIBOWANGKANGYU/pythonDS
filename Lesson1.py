# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 19:59:11 2019

@author: kangyuwang
"""

#Point
from shapely.geometry import Point, LineString, Polygon
point1=Point(2.2, 4.2)
point2=Point(7.2, -25.1)
point3 = Point(9.26, -2.456)
point3D = Point(9.26, -2.456, 0.57)
point_type=type(point1)

print(point1)
print(point3D)
print(point_type)

##Point coordinates
point_coords=point1.coords
type(point_coords)
point_coords.xy#a tuple
point1.x
point1.y
point_dist=point1.distance(point2)
print("Distance between the two points are {0:.2f} decimal degrees".format(point_dist))

#Linestring
line=LineString([point1, point2, point3])
line2 = LineString([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
print(line)
print(line2)
type(line)
lxy=line.xy
print(lxy)
linex=lxy[0]
print(linex)
l_length= line.length
l_centroid=line.centroid
print("Length of our line is {0: .2f} decimal degrees".format(l_length))
print("Centroid of our line is at {}".format(l_centroid))

#Polygon
poly=Polygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
poly2=Polygon([[p.x, p.y]for p in [point1, point2, point3]])
poly_type=poly.geom_type
poly2_type=type(poly2)
print(poly)# Double parentheses
print(poly2)
print(poly_type)
print(poly2_type)

##Polygon with a hole
world_exterior= [(-180, 90), (-180, -90), (180, -90), (180, 90)]
hole=[[(-170, 80), (-170, -80), (170, -80), (170, 80)]]
world=Polygon(world_exterior)
world_has_a_hole=Polygon(shell=world_exterior, holes=hole)
print(world)
print(world_has_a_hole)

##Polygon attributes and functions
world_centroid=world.centroid
world_area=world.area
world_bbox=world.bounds
world_ext=world.exterior
world_ext_length=world.exterior.length

print("Poly Centroid:", world_centroid)
print("Poly Area", world_area)
print("Poly Bounding Box:", world_bbox)
print("Poly Exterior:", world_ext)
print("Poly Exterior Length:", world_ext_length)

# Geometry collections
from shapely.geometry import MultiPoint, MultiPolygon, MultiLineString, box
multi_point=MultiPoint([point1, point2, point3])
multi_point2=MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
line1=LineString([point1, point2])
line2=LineString([point2, point3])
multi_line=MultiLineString([line1, line2])
west_exterior=[(-180, 90), (-180, -90), (0, -90), (0, 90)]
west_hole=[[(-170 ,80), (-170, -80), (0, -80), (0, 80)]]
west_poly=Polygon(shell=west_exterior, holes=west_hole)
minx, miny=0, -90
maxx, maxy=180, 90
east_poly_box=box(minx=minx, miny=miny, maxx=maxx, maxy=maxy)
multi_poly=MultiPolygon([west_poly, east_poly_box])

print(multi_point)
print(multi_point2)
print(multi_line)
print(multi_poly)

##Attributes
convex=multi_point.convex_hull
print(convex)
lines_count=len(multi_line)
multi_poly_area=multi_point.area
west_area=multi_poly[0].area
valid=multi_poly.is_valid# The polygon is not valid

print(convex)
print(lines_count)
print(multi_poly_area)
print(west_area)
print(valid)
