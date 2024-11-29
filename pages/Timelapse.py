import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from data_analysis.test_code import data_handler

myDH = data_handler.dataHandler()

all_data = pd.concat(myDH.unique.values())

all_data["timestamp"] = pd.to_datetime(all_data["timestamp"])

# Sidebar configuration
st.set_page_config(page_title="Animal Movement Paths", layout="wide")
st.sidebar.header("Filter Options")

# Select one category for analysis
categories = all_data["name"].unique()
selected_category = st.sidebar.selectbox("Select category:", categories, index=0)

# Filter data for the selected category
filtered_data = all_data[all_data["name"] == selected_category]

# Sort data by timestamp for animation
filtered_data = filtered_data.sort_values("timestamp")

# Prepare persistent dots by duplicating data for animation
persistent_data = pd.DataFrame()
for i, timestamp in enumerate(filtered_data["timestamp"].unique()):
    # For each timestamp, include all previous data
    snapshot = filtered_data[filtered_data["timestamp"] <= timestamp].copy()
    snapshot["animation_frame"] = timestamp
    persistent_data = pd.concat([persistent_data, snapshot])

# Distinguish most recent datapoint  - doesnt work 
persistent_data["dot_type"] = persistent_data.groupby("animation_frame").cumcount() + 1
persistent_data["color"] = persistent_data["animation_frame"].apply(
    lambda x: "red" if x == persistent_data["animation_frame"].max() else "lightgray"
)

latitude_center = persistent_data["location-lat"].mean()
longitude_center = persistent_data["location-long"].mean()

# Create time-based scatter map with persistent dots
st.header("Animal Movement Timelapse")
st.subheader(f"Tracking Movement: {selected_category}")

animated_map = px.scatter_mapbox(
    persistent_data,
    lat="location-lat",
    lon="location-long",
    color="color", # yeah literally doesnt work 
    hover_name="name",
    hover_data={"timestamp": True, "dot_type": True},
    animation_frame=persistent_data["animation_frame"].dt.strftime("%Y-%m-%d %H:%M:%S"),
    zoom=10,
    center={"lat": latitude_center, "lon": longitude_center},
    title="Animal Movement Path",
)

animated_map.update_traces(marker=dict(size=20))  
animated_map.update_layout(
    mapbox_style="open-street-map",
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    showlegend=False, 
)

# Display the map
st.plotly_chart(animated_map, use_container_width=True)
