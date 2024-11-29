from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Slider
from bokeh.layouts import layout
import pandas as pd

# Load your dataset
data = pd.read_csv("red_fox.csv", parse_dates=['timestamp'])

# Prepare the data for the first frame
source = ColumnDataSource(data[data['timestamp'] == data['timestamp'].min()])

# Create a figure
p = figure(
    title="Interactive Map with Slider",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tools="pan,wheel_zoom,reset",
)

# Add points to the figure
p.circle(
    x='location-long',
    y='location-lat',
    size=10,
    color="blue",
    source=source,
)

# Slider to control the timestamp
slider = Slider(
    start=0,
    end=len(data['timestamp'].unique()) - 1,
    step=1,
    value=0,
    title="Timestamp Index"
)

# Update function for the slider
def update(attr, old, new):
    current_time = data['timestamp'].unique()[slider.value]
    new_data = data[data['timestamp'] == current_time]
    source.data = ColumnDataSource(new_data).data

slider.on_change("value", update)

# Arrange layout and display
curdoc().add_root(layout([[p], [slider]]))
