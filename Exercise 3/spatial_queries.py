# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 21:38:28 2019

@author: kangyuwang
"""

#Exercise 3
##Geocoding shopping centers
import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
from fiona.crs import from_epsg
import matplotlib.pyplot as plt
from shapely.geometry import Point
fp='C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/shopping_centers.txt'
data = pd.read_csv(fp, sep=";", header= 0)
geo=geocode(data.loc[:,'addr'], provider="nominatim")
data_geo=gpd.GeoDataFrame(geo)
print(data_geo.crs)# There is no projection information
data_geo.crs=from_epsg(4236)# set a crs (WGS 84) on the object first
data_geo=data_geo.to_crs(epsg=3879)
data_geo=data_geo.join(data)
data_geo = data_geo.drop(columns="addr")
data_geo.to_file("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/shopping_centers.shp")
data_geo.plot()
##Creating buffers
data_geo.assign(buffer=None)
data_geo.loc[:, 'buffer']=data_geo.loc[:, 'geometry'].apply(lambda point : point.buffer(distance=5000))
data_geo.loc[:, 'geometry']=data_geo.loc[:, 'buffer']
data_geo.drop('buffer', axis=1)
##How many people living in the buffer areas 
pop=gpd.read_file("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/Vaestotietoruudukko_2015.shp")
pop=pop.loc[:, ['ASUKKAITA','geometry']]
print(pop.crs)
pop=pop.to_crs(epsg=3879)
join = gpd.sjoin(data_geo, pop, how="right")
sum_pop=join.groupby('name').agg(sum_pop=pd.NamedAgg(column='ASUKKAITA', aggfunc=sum))
print(sum_pop)
##Closest shopping center
activity = pd.read_csv("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/activity_locations.txt", sep=";", header= 0)
geo_activity=geocode(activity.loc[:,'addr'], provider="nominatim")
geo_activity=geo_activity.join(activity)
geo_activity=geo_activity.drop('addr', axis=1)
print(geo_activity.crs)# There is no projection information
geo_activity.crs=from_epsg(4236)# set a crs (WGS 84) on the object first
geo_activity=geo_activity.to_crs(epsg=3879)
[min([s.distance(t) for t in data_geo.iloc[:,0].tolist()]) for s in geo_activity.iloc[:,0].tolist()]