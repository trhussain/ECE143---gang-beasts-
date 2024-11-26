import pandas as pd
import folium

# Example DataFrame
df = pd.DataFrame({
    'latitude': [37.7749, 34.0522, 40.7128],
    'longitude': [-122.4194, -118.2437, -74.0060],
    'info': ['San Francisco', 'Los Angeles', 'New York']
})

# Convert DataFrame to GeoJSON
def df_to_geojson(df, lat='latitude', lon='longitude', properties=None):
    geojson = {"type": "FeatureCollection", "features": []}
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row[lon], row[lat]]
            },
            "properties": {prop: row[prop] for prop in properties or []}
        }
        geojson["features"].append(feature)
    return geojson

geojson_data = df_to_geojson(df, lat='latitude', lon='longitude', properties=['info'])

# Create a Folium map
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)

# Add GeoJSON layer
folium.GeoJson(
    geojson_data,
    name="Locations",
    popup=folium.GeoJsonPopup(fields=["info"])
).add_to(m)

# Display the map
m
