import streamlit as st
import folium
from streamlit_folium import st_folium
from data import data_handler


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

myDH = data_handler.dataHandler()
df = myDH.desired_df
# myDH.displayDat
# aPretty()
data_points = [
    {"lat": 37.7749, "lon": -122.4194, "name": "SF", "info": "ahahahah"},
    {"lat": 34.0522, "lon": -118.2437, "name": "LA", "info": "lolololol"},
    {"lat": 40.7128, "lon": -74.0060, "name": "NYC", "info": "heyeyeyeyyee"}
]
# m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=5, tiles="OpenStreetMap")
m = folium.Map(location=[37.7749, -122.4194], zoom_start=5, tiles="OpenStreetMap")
 
for point in data_points:
    add_circle_marker(m,point["lat"], point["lon"], point['info'])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # folium.CircleMarker(
    #     location=[point["lat"], point["lon"]],
    #     radius=10, 
    #     color = "blue",
    #     fill = True,
    #     fill_color="blue", 
    #     fill_opacity=0.8,        
    #     popup=folium.Popup(point["name"], parse_html=True),

    #     tooltip=f"{point['name']}: {point['info']}"
    # ).add_to(m)
    
# for index, row in df.iterrows():

#     folium.CircleMarker(
#         location=[row['LON'], row['LAT']],
#         radius=5, 
#         color = "blue",
#         fill = True,
#         fill_color="blue", 
#         fill_opacity=0.8,        
#         popup=folium.Popup(row['info'], parse_html=True),
#         tooltip=f"{row['info']}"
#     ).add_to(m)    
    
    
    
    
st_folium(m, width=700, height=500)
