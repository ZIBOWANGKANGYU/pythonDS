# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 20:12:58 2019

@author: kangyuwang
"""
from shapely.geometry import Point, LineString, Polygon

def getCentroid(x):
    return x.centroid

def getArea(x):
    return x.area

def getLength(x):
    if type(x)==LineString:
        return x.length
    if type(x)==Polygon:
        return x.exterior.length
    else:
        raise Error("Error: LineString or Polygon geometries required!")
        
