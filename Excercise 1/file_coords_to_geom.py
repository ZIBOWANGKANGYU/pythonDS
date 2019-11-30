# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 20:47:11 2019

@author: kangyuwang
"""

import pandas as pd
import statistics as sta
from shapely.geometry import Point, LineString
data = pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Excercise 1/travelTimes_2015_Helsinki.txt', sep=";", header = 0)
data['from_id']
coords=data.loc[:, ['from_x', 'from_y', 'to_x', 'to_y']]
orig_points=[Point(coords.iloc[n, 0], coords.iloc[n, 1]) for n in range(0, coords.shape[0])]
dest_points=[Point(coords.iloc[n, 2], coords.iloc[n, 3]) for n in range(0, coords.shape[0])]
lines=[LineString([orig_points[i], dest_points[i]]) for i in range(0, coords.shape[0])]
sta.mean(lines[i].length for i in range(0, coords.shape[0]))
