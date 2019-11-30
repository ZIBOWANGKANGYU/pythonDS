# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:38:13 2019

@author: kangyuwang
"""
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
def col_select(df, cols):
    col_select=df.loc[:, cols]
    return col_select
import pysal as ps
#Problem 1
TT_Jumbo=pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/TravelTimes_to_5878070_Jumbo.txt', sep=";")
TT_Jumbo=col_select(TT_Jumbo, ["pt_r_tt", "car_r_t", "from_id", "to_id"])

TT_Dixi=pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/TravelTimes_to_5878087_Dixi.txt', sep=";")
TT_Dixi=col_select(TT_Dixi, ["pt_r_tt", "car_r_t", "from_id", "to_id"])


TT_Myyrmanni=pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/TravelTimes_to_5902043_Myyrmanni.txt', sep=";")
TT_Myyrmanni=col_select(TT_Myyrmanni, ["pt_r_tt", "car_r_t", "from_id", "to_id"])

TT_Itis=pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/TravelTimes_to_5944003_Itis.txt', sep=";")
TT_Itis=col_select(TT_Itis, ["pt_r_tt", "car_r_t", "from_id", "to_id"])

TT_Forum=pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/TravelTimes_to_5975373_Forum.txt', sep=";")
TT_Forum=col_select(TT_Forum, ["pt_r_tt", "car_r_t", "from_id", "to_id"])

TT_Iso_omena=pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/TravelTimes_to_5978593_Iso_omena.txt', sep=";")
TT_Iso_omena=col_select(TT_Iso_omena, ["pt_r_tt", "car_r_t", "from_id", "to_id"])

TT_Ruoholahti=pd.read_csv('C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/TravelTimes_to_5980260_Ruoholahti.txt', sep=";")
TT_Ruoholahti=col_select(TT_Ruoholahti, ["pt_r_tt", "car_r_t", "from_id", "to_id"])

map_raw=gpd.read_file("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/dataE4/MetropAccess_YKR_grid_EurefFIN.shp")
map_Jumbo=map_raw.merge(TT_Jumbo, left_on='YKR_ID', right_on='from_id', how='left')

map_Jumbo.loc[:, 'car_r_t_classify']=(map_Jumbo.loc[:, 'car_r_t']>=map_Jumbo.loc[:, 'car_r_t'].mean())
map_Jumbo.plot(column="car_r_t_classify")
plt.tight_layout()

#Problem 2
def combine_accessibility(geo_df, accessibility_df, name_center):
    geo_df=geo_df.merge(accessibility_df, left_on='YKR_ID', right_on='from_id', how='left')
    geo_df.loc[:, name_center+'pt']=geo_df.loc[:, 'pt_r_tt']
    geo_df.loc[:, name_center+'car']=geo_df.loc[:, 'car_r_t']
    geo_df=geo_df.drop(['from_id'], axis=1)
    geo_df=geo_df.drop(['to_id'], axis=1)
    geo_df=geo_df.drop(['pt_r_tt'], axis=1)
    geo_df=geo_df.drop(['car_r_t'], axis=1)
    return geo_df
    
map_raw=combine_accessibility(geo_df=map_raw, accessibility_df=TT_Jumbo, name_center="5878070")
map_raw=combine_accessibility(geo_df=map_raw, accessibility_df=TT_Dixi, name_center="5878087")
map_raw=combine_accessibility(geo_df=map_raw, accessibility_df=TT_Myyrmanni, name_center="5902043")
map_raw=combine_accessibility(geo_df=map_raw, accessibility_df=TT_Itis, name_center="5944003")
map_raw=combine_accessibility(geo_df=map_raw, accessibility_df=TT_Forum, name_center="5975373")
map_raw=combine_accessibility(geo_df=map_raw, accessibility_df=TT_Iso_omena, name_center="5978593")
map_raw=combine_accessibility(geo_df=map_raw, accessibility_df=TT_Ruoholahti, name_center="5980260")

map_raw.loc[:, 'min_time_pt']=map_raw.loc[:, ['5878070pt', '5878087pt', '5902043pt', '5944003pt','5975373pt','5978593pt','5980260pt']].min(axis=1)
list_names=['5878070pt', '5878087pt', '5902043pt', '5944003pt','5975373pt','5978593pt','5980260pt']
map_raw.loc[:, 'dominant_service']=[[i for indx,i in enumerate(list_names) if (map_raw.loc[j, ['5878070pt', '5878087pt', '5902043pt', '5944003pt','5975373pt','5978593pt','5980260pt']]==map_raw.loc[j, ['5878070pt', '5878087pt', '5902043pt', '5944003pt','5975373pt','5978593pt','5980260pt']].min())[indx] == True][0][0:6] for j in range(len(map_raw.index))]
map_raw.loc[:, 'dominant_service']=map_raw.loc[:, 'dominant_service'].astype('int')
map_raw.plot(column="min_time_pt", scheme="Fisher_Jenks", k=6, cmap="RdYlBu", linewidth=0, legend=True)
map_raw.plot(column="dominant_service")

# Problem 3
pop=gpd.read_file("C:/Users/kangyuwang/OneDrive/portfolio/python_geo/Exercise 3/Vaestotietoruudukko_2015.shp")
ds_agg=map_raw.loc[:, ['geometry', 'dominant_service']].dissolve(by='dominant_service')
ds_agg.loc[:, "dominant_service"]=ds_agg.index
ds_agg_proj=ds_agg.copy()
ds_agg_proj=ds_agg_proj.to_crs(epsg=3879)
pop_proj=pop.copy()
pop_proj=pop_proj.to_crs(epsg=3879)
pop_within_ds = gpd.sjoin(pop_proj, ds_agg_proj, op="within", how='right')
pop_agg=pop_within_ds.loc[:, ['geometry', 'ASUKKAITA', 'dominant_service']].dissolve(by='dominant_service', aggfunc='sum')
