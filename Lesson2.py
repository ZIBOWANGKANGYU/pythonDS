# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 23:46:09 2019

@author: kangyuwang
"""
#Importing a shape file
import geopandas as gpd
sp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Data/Data/DAMSELFISH_distributions.shp"
data=gpd.read_file(sp)
type(data)
data.head()
data.plot()

#Writing a shape file
out="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Data/Data/DAMSELFISH_distributions_SELECTION.shp"
selection=data.iloc[0:50]
selection.to_file(out)

#Geometries in Geopandas
data.loc[:,"geometry"].head()
selection=data.iloc[0:5, ]
next(selection.iterrows())
for index, row in selection.iterrows():
    poly_area=row["geometry"].area
    print("Polygon area at index {0} is: {1: 2f}".format(index, poly_area))

##Creating a new column
data.area #Using Geoframe.area attribute
data['area']=data.area
data.loc[:, 'area'].head(2)
max_area=data['area'].max()
mean_area=data['area'].mean()
print("Max area: {0: 2f}\nMean area: {1: 2f} ".format(max_area, mean_area))

#Creating geometries into a GeoDataFrame
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import fiona
newdata=gpd.GeoDataFrame()
newdata
newdata['geometry']=None
newdata

coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly=Polygon(coordinates)
poly
newdata.loc[0, "geometry"]=poly
newdata
newdata.loc[0, "Location"]='Senaatintori'
newdata
##determine the coordinate reference system
print(newdata.crs)
from fiona.crs import from_epsg
newdata.crs=from_epsg(4236)
newdata.crs

# Save multiple shapefiles
sp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Data/Data/DAMSELFISH_distributions.shp"
data=gpd.read_file(sp)
grouped=data.groupby('BINOMIAL')
grouped # similar to a list of keys and values
for key, values in grouped:
    individual_fish=values
individual_fish
type(individual_fish)
print(key)
##Save files
Outfolder="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Results/"
for key, values in grouped:
    outName="{}.shp".format(key).replace(" ", "_")
    print("Processing: {}".format(key))
    outpath=Outfolder+outName
    values.to_file(outpath)
    
# Coordinate reference system 
fp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Europe_borders/Europe_borders.shp"
data=gpd.read_file(fp)
data.crs
data.loc[:,'geometry'].head(2)
data_proj=data.copy()
data_proj=data_proj.to_crs(epsg=3035)
data_proj.loc[:,'geometry'].head()
##Ploting
import matplotlib.pyplot as plt
data.plot(facecolor="grey")
plt.title("WSG84 projection")
plt.tight_layout()
data_proj.plot(facecolor="blue")
plt.title("ETRS Lambert Azimuthal Equal Area projection")
plt.tight_layout()
##Change crs setting
from fiona.crs import from_epsg
data_proj.crs=from_epsg(3035)
data_proj.crs
outfp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Europe_borders/Europe_borders_epsg3035.shp"
data_proj.to_file(outfp)
