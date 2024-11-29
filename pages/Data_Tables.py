import streamlit as st
import pandas as pd
from data_analysis.test_code.data_handler import dataHandler

myDH = dataHandler()

st.set_page_config(page_title="Data Tables", page_icon="📄")
st.title("Data Tables")
st.header("Tables by Category")

unique_tables = myDH.unique

col1, col2 = st.columns(2)

# Alternate placing tables in the two columns
for i, (table_name, table_data) in enumerate(unique_tables.items()):
    if i % 2 == 0:  # Add to the first column
        with col1:
            st.subheader(table_name)
            st.dataframe(table_data)
    else:  # Add to the second column
        with col2:
            st.subheader(table_name)
            st.dataframe(table_data)
