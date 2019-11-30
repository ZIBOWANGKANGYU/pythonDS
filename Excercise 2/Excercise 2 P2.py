# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:58:13 2019

@author: kangyuwang
"""

import pandas as pd
from shapely.geometry import Point, LineString, Polygon

data=pd.read_csv("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Excercise 2/some_posts.csv")
data['geometry']=None
for index, row in data.iterrows():
    data.loc[index, 'geometry']=Point(row['lat'], row['lon'])
    
import geopandas as gpd
from fiona.crs import from_epsg
import matplotlib.pyplot plt
data_gdf=gpd.GeoDataFrame(data)
data_gdf.crs=from_epsg(4236)
data_gdf.to_file("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Excercise 2/Kruger_posts.shp")
data_gdf.plot()

data_gdf_proj=data_gdf.to_crs(epsg=32735)
data_gdf_proj_grp=data_gdf_proj.groupby('userid')
movements=gpd.GeoDataFrame()
for key, values in data_gdf_proj_grp:
    values_sort=values.sort_values(by=['timestamp'])
    if len(values_sort.index)>1:
        line=LineString((values_sort.loc[values_sort.index[i], 'lat'], values_sort.loc[values_sort.index[i], 'lon']) for i in range(len(values_sort.index)))
        movements=movements.append(pd.DataFrame(data={'geometry': [line], 'userid': [key], 'distance': line.length}), ignore_index=True)
    else: 
        movements=movements.append(pd.DataFrame(data={'geometry': None, 'userid': [key], 'distance':None}), ignore_index=True)
movements_gdf=gpd.GeoDataFrame(movements)
movements_gdf.to_file("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Excercise 2/Some_movements.shp")
##answers to question
movements.loc[: ,'distance'].mean()
movements.loc[: ,'distance'].max()
movements.loc[: ,'distance'].min()
