# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:45:54 2019

@author: kangyuwang
"""
from shapely.geometry import Point, LineString, Polygon
def createPointGeom(x_coord, y_coord):
    point=Point(x_coord, y_coord)
    return point
def createLineGeom(list_point):
    linestring=LineString(list_point)
    return linestring
def createPolyGeom(x):
    if type(x[0])==tuple:
        polygon=Polygon(x)
    if type(x[0])==Point:
        polygon=Polygon([(p.x, p.y) for p in x])
    return polygon
createPolyGeom(input2)
