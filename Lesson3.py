# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:03:34 2019

@author: kangyuwang
"""
#Geocoding
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
data=pd.read_csv("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/addresses.txt", sep=';')
data.head()
from geopandas.tools import geocode
geo=geocode(data.loc[:,'addr'], provider="nominatim")
geo.head(2)
join=pd.concat([data, geo], axis=1)
join=gpd.GeoDataFrame(join)
type(join)
outfp = "C:/Users/kangyuwang/OneDrive/portfolio/python_geo/addresses.shp"
join.to_file(outfp)
from fiona.crs import from_epsg
join.crs=from_epsg(4326)
join_epsg3879=join.to_crs(epsg=3879)
outfp = 'C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/addresses_epsg3879.shp'
join_epsg3879.to_file(outfp)
##Making map
join.plot()
plt.tight_layout()

#Retriving OpenStreetMap data
import osmnx as ox
import matplotlib.pyplot as plt
place_name='Kamppi, Helsinki, Finland'
graph=ox.graph_from_place(place_name)
type(graph)#networkx is a module used to analyze complex networks
fig, ax=ox.plot_graph(graph)
plt.tight_layout()
##Download other types of OSM data
area=ox.gdf_from_place(place_name)
footprint=ox.footprints_from_place(place_name)#This replaces ox.buildings_from_place
type(area)
type(footprint)
nodes, edges=ox.graph_to_gdfs(graph)
nodes.head()
edges.head()
##Cerate a map out of the streets
fig, ax=plt.subplots()
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')
footprint.plot(ax=ax, facecolor='khaki', alpha=0.7)
plt.tight_layout()
##Subset the edges layer 
edges_cycleway=edges.loc[edges['highway'] == 'cycleway']
fig, ax=plt.subplots()
area.plot(ax=ax, facecolor='black')
edges_cycleway.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')
footprint.plot(ax=ax, facecolor='khaki', alpha=0.7)
plt.tight_layout()

#Data reclassification
fp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/data_l3/data/Corine2012_Uusimaa.shp"
data=gpd.read_file(fp)
data.head(2)
data.columns
data=data.loc[:, ['Level1', 'Level1Eng', 'Level2', 'Level2Eng', 'Level3', 'Level3Eng', 'Luokka3', 'geometry']]
data.columns
data.plot(column='Level3', linewidth=0.05)
plt.tight_layout()
##What valeus we have in 'Level3'
list(data.loc[:, 'Level3Eng'].unique())
##Select only lakes
lakes=data[data.loc[:, 'Level3Eng']=="Water bodies"]
lakes.head(2)
##check coordinate reference systems information
data.crs# Units are in meters and we have UTM projection
lakes=lakes.assign(area=lakes.area)
lakes.loc[:, 'area'].head(2)
lakes=lakes.assign(area_km2=lakes.loc[:,'area']/1000000)
l_mean_area=lakes.loc[:, 'area_km2'].mean()
l_mean_area
##Creating a customized classifier 
def BinaryClassfieir (row, source_col, output_col, threashold):
    if row[source_col]<threashold:
        row[output_col]=0
    else: 
        row[output_col]=1
    return row
lakes=lakes.assign(small_big=None)
lakes=lakes.apply(BinaryClassfieir, source_col="area_km2", output_col="small_big", threashold=l_mean_area, axis=1) #calls lambda function for each row
##Plot the lakes
lakes.plot(column="small_big", linewidth=0.05, cmap="seismic")
plt.tight_layout()
##Save the lakes file
outfp_lakes="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/data_l3/data/lakes.shp"
lakes.to_file(outfp_lakes)
##Multicriteria classification
def customClassifier2(row, src_col1, src_col2, threshold1, threshold2, output_col):
    if row[src_col1]<threshold1 and row[src_col2]>threshold2:
        row[output_col]=1
    else:
        row[output_col]=0
    return row
fp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/data_l3/data/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"
acc=gpd.read_file(fp)
acc.head(2)
acc.columns
acc=acc[acc.loc[:, 'pt_r_tt']>=0]
import matplotlib.pyplot as plt
acc.plot(column='pt_r_tt', scheme="Fisher_Jenks", k=9, cmap="RdYlBu", linewidth=0)
plt.tight_layout()
##Mapping walking distance
acc.plot(column='walk_d', scheme="Fisher_Jenks", k=9, cmap="RdYlBu", linewidth=0)
plt.tight_layout()
##multiple criteria selection
acc=acc.assign(Suitable_area=None)
acc=acc.apply(customClassifier2, src_col1='pt_r_tt', src_col2='walk_d', threshold1=20, threshold2=4000, output_col='Suitable_area', axis=1)
acc.head()
acc.loc[:, 'Suitable_area'].value_counts()
acc.plot(column='Suitable_area', line)
plt.tight_layout()

