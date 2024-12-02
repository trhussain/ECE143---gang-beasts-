import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from data_analysis.test_code import data_handler

myDH = data_handler.dataHandler()

all_data = pd.concat(myDH.unique.values())
all_data["timestamp"] = pd.to_datetime(all_data["timestamp"])

min_time = all_data["timestamp"].min()
max_time = all_data["timestamp"].max()

# Streamlit configs
st.set_page_config(page_title="Animal Tracking Maps", layout="wide")
st.sidebar.header("Filter by Time")

# Time slider for filtering
time_range = st.sidebar.slider(
    "Select time range:",
    min_value=min_time.to_pydatetime(),
    max_value=max_time.to_pydatetime(),
    value=(min_time.to_pydatetime(), max_time.to_pydatetime()),
    format="MM/DD/YY - hh:mm",
)

# Filter the data based on the selected time range
filtered_data = all_data[
    (all_data["timestamp"] >= time_range[0]) & (all_data["timestamp"] <= time_range[1])
]

col1, col2 = st.columns(2)

# Map configuration
latitude_center = filtered_data["location-lat"].mean()
longitude_center = filtered_data["location-long"].mean()

# Dot Plot 
with col1:
    st.header("Dot Plot")
    dot_map = px.scatter_mapbox(
        filtered_data,
        lat="location-lat",
        lon="location-long",
        color="name",  
        hover_name="name",
        hover_data={"timestamp": True},
        zoom=10,
        
        center={"lat": latitude_center, "lon": longitude_center},
        title="Animal Dot Map",
        
    )
    dot_map.update_layout(
        mapbox_style="open-street-map",
        height=500,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )
    dot_map.update_traces(marker=dict(size=20))
    st.plotly_chart(dot_map, use_container_width=True)

# Heatmap 
with col2:
    st.header("Heatmap")
    heatmap = px.density_mapbox(
        filtered_data,
        lat="location-lat",
        lon="location-long",
        z=None,  
        radius=20,  #
        zoom=10,
        center={"lat": latitude_center, "lon": longitude_center},
        title="Animal Heatmap",
    )
    heatmap.update_layout(
        mapbox_style="open-street-map",
        height=500,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )
    st.plotly_chart(heatmap, use_container_width=True)

# Display selected time range below the maps
st.sidebar.write(f"Showing data from **{time_range[0]}** to **{time_range[1]}**")
