import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}
df = pd.DataFrame(data)

# Create a Plotly Table
fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(df.columns),
        fill_color="lightgrey",
        align="left"
    ),
    cells=dict(
        values=[df[col] for col in df.columns],
        fill_color="white",
        align="left",
        # Tooltip: add hover text
    )
)])

# Display the table in Streamlit
st.plotly_chart(fig, use_container_width=True)
