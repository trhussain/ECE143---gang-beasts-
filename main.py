import streamlit as st
import folium
from streamlit_folium import st_folium
from data import data_handler
import time
import pandas as pd
import geopandas
import folium
import geodatasets

from folium import plugins



def add_circle_marker(map_object, lat, lon, info, color = "red", radius=5, info2 = None, info3 = None):
    
    info2_display = info2 if info2 is not None else ""
    info3_display = info3 if info3 else ""
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        color=color,
        fill=True,
        fill_color= color,
        fill_opacity=0.5,
        opacity = 0.1,
        popup=folium.Popup(info, parse_html=True),
        tooltip=f"{info} \n {info2_display}"
    ).add_to(map_object)

def plotDot(point):
    folium.CircleMarker(
        location=[point['LAT'], point['LON']],
        radius=5,
        weight=2,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6,
        popup=folium.Popup(f"{point['info']}", parse_html=True),  # Add info to popup
        tooltip=f"{point['info']}"  # Add info to tooltip
    ).add_to(m)

    
myDH = data_handler.dataHandler()
df = myDH.desired_df

data_points = [
    {"lat": 37.7749, "lon": -122.4194, "name": "SF", "info": "ahahahah"},
    {"lat": 34.0522, "lon": -118.2437, "name": "LA", "info": "lolololol"},
    {"lat": 40.7128, "lon": -74.0060, "name": "NYC", "info": "heyeyeyeyyee"}
]
df2 = pd.DataFrame()
latMean = df['LAT'].mean()
lonMean = df['LON'].mean()


m = folium.Map(location=[latMean, lonMean], zoom_start=5, tiles="OpenStreetMap")

for point in data_points:
    add_circle_marker(m,point["lat"], point["lon"], point['info'])
lat_lon_pairs = list(zip(df['LAT'], df['LON'], df['name']))    
# myDH.displayDataPretty()
for point in lat_lon_pairs: 
    add_circle_marker(m,point[0], point[1], point[2])

    # print(point[0])
st_folium(m, width=700, height=500)
