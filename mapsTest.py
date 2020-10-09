# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:15:16 2020

@author: Administrator
"""

import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
import time
import streamlit as st
from pytrends.request import TrendReq
from datetime import datetime

usa = gpd.read_file('./states_21basic/states.shp')

def state_plotter(states, us_map=True):
    fig,ax = plt.subplots(figsize=(30,30))
    if us_map:
        if 'HI' in states:
            usa[0:50].plot(ax=ax, alpha = 0.3)
        elif 'AK' in states:
            usa[1:51].plot(ax=ax, alpha = 0.3)
        elif 'AK' and 'HI' in states:
            usa[0:51].plot(ax=ax, alpha = 0.3)
        else:
            usa[1:50].plot(ax=ax, alpha = 0.3)
            
        for n in states:
            usa[usa.STATE_ABBR == f'{n}'].plot(ax=ax, edgecolor = 'y', linewidth = 2)
            
    elif us_map == False:
        for n in states:
            usa[usa.STATE_ABBR == f'{n}'].plot(ax=ax,edgecolor = 'y', linewidth = 2)
            
            
"""
Google Trends Data
"""

pytrends = TrendReq(hl = 'en-US', tz = 360)

df2 = ['Timberland Boots']

dataset = [] 

begin_date = st.sidebar.date_input(
    'Enter start date',
    value = datetime(2020,1,1),)

end_date = st.sidebar.date_input(
    'Enter end date',
    value = datetime(2020,6,1),)

searchDates = begin_date.strftime('%Y-%m-%d')+' '+end_date.strftime('%Y-%m-%d')

for x in range(0, len(df2)):
    keywords = [df2[x]]
    pytrends.build_payload(kw_list = keywords,
                            cat = 0,
                            timeframe = searchDates,
                            geo = 'US')
    data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol = False, inc_geo_code = False)
    if not data.empty:
        dataset.append(data)
        
dataset = pd.concat(dataset, axis = 1)

dataset = dataset.rename(columns = {'Timberland Boots': 'TBL'})

df = usa.merge(dataset, left_on='STATE_NAME', right_on='geoName')

fig,ax = plt.subplots(1, 1)

df[1:50].plot(column = 'TBL',
         ax = ax,
         legend = True,
         legend_kwds={'label': "Trend Popularity by State",
                      'orientation': 'horizontal'})

st.title('Trend Data by State for TBL')

if st.checkbox('Show raw data?'):
    map_df = pd.DataFrame(df.drop(columns='geometry'))
    st.subheader('Raw data')
    st.write(map_df)

st.pyplot(fig)
