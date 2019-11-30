# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 22:10:58 2019

@author: kangyuwang
"""
#Point inside polygon
from shapely.geometry import Point, Polygon
p1=Point(24.952242, 60.1696017)
p2=Point(24.976567, 60.1612500)
coords=[(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly = Polygon(coords)
p1.within(poly)
p2.within(poly)
poly.contains(p1)
poly.contains(p2)

#Intersect
from shapely.geometry import LineString, MultiLineString
line_a=LineString([(0, 0), (1, 1)])
line_b=LineString([(1, 1), (0, 2)])
line_a.intersects(line_b)
multi_line=MultiLineString([line_a, line_b])
multi_line
line_a.touches(line_a)

#Point in polygon using geopandas
import geopandas as gpd
fp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/addresses.shp"
data=gpd.read_file(fp)
import matplotlib.pyplot as plt
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
fp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/PKS_suuralue.kml"
polys=gpd.read_file(fp)
polys
##select the southern district
southern=polys[polys.loc[:, 'Name']=='Eteläinen']
southern.reset_index(drop=True, inplace=True)
fig, ax=plt.subplots()
polys.plot(ax=ax, facecolor='grey')
southern.plot(ax=ax, facecolor='red')
data.plot(ax=ax, color='blue', markersize=5)
plt.tight_layout()
##Get points in the southern district
import shapely.speedups
shapely.speedups.enable()
pip_mask=data.within(southern.loc[0, 'geometry'])
pip_mask
pip_data=data[pip_mask]
pip_data
fig, ax=plt.subplots()
polys.plot(ax=ax, facecolor='grey')
southern.plot(ax=ax, facecolor='red')
pip_data.plot(ax=ax, color='blue', markersize=5)
plt.tight_layout()
#Spatial join
import geopandas as gpd
fp="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/Vaestotietoruudukko_2015.shp"
pop=gpd.read_file(fp)
pop=pop.rename(columns={'ASUKKAITA':'pop15'})
pop=pop.loc[:, ["pop15", "geometry"]]
pop.head()
##Join the layers
addr_fp='C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/addresses_epsg3879.shp'
addresses=gpd.read_file(addr_fp)
addresses.head()
print(addresses.crs)
print(pop.crs)
join=gpd.sjoin(addresses, pop, how='inner', op='within')
join.head()
join.to_file('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/addresses_pop15_epsg3979.shp')

import matplotlib.pyplot as plt
join.plot(column='pop15', cmap='Reds', markersize=7, scheme='fisher_jenks', legend=True)
plt.title("Amount of inhabitants living close the the point")
plt.tight_layout()
#Nearest neighbor analysis
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
orig=Point(1, 1.67)
dest1, dest2, dest3 = Point (0, 1.45), Point(2, 2), Point(0, 2.5)
destinations=MultiPoint([dest1, dest2, dest3])
print(destinations)
nearest_geoms=nearest_points(orig, destinations)
print(nearest_geoms[0])##The original spot
print(nearest_geoms[1])
#Nearest point using gepandas
def nearest(row, geom_union, df1, df2, geom1_col='geometry', geom2_col='geometry', src_column=None):
    nearest = (df2.loc[:,geom2_col]==nearest_points(row[geom1_col], geom_union)[1])
    value=df2[nearest][src_column].to_numpy()[0]
    return value
fp1='C:/Users/kangyuwang/OneDrive/portfolio/python_geo/PKS_suuralue.kml'
fp2="C:/Users/kangyuwang/OneDrive/portfolio/python_geo/addresses.shp"
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'    
df1=gpd.read_file(fp1, driver="KML")   
df2=gpd.read_file(fp2)   
unary_union=df2.unary_union
print(unary_union)    
df1.loc[:,'centroid']=df1.centroid
##Find the closest points
df1.loc[:, 'nearest_id']=df1.apply(nearest, geom_union=unary_union, df1=df1, df2=df2, geom1_col='centroid', src_column='id', axis=1)
df1.head()

    
    
    
    
    
    
    
    