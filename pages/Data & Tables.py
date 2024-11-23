import streamlit as st
from data.data_handler import dataHandler

myDH = dataHandler()

st.set_page_config(page_title="Data tables", page_icon="📄")
# Create columns with equal width to center an element
col2, col3 = st.columns([50, 50])  # Adjust ratios as needed

with col2:  # Center column
    st.title("Maps")
    # st.write("Raw Data")
    # st.map(myDH.raw_df)
    st.write("Processed Data")
    st.map(myDH.desired_df)

with col3:
    st.title("Tables")
    st.write("")
    st.write("")
    st.write("")

    st.dataframe(myDH.desired_df)
