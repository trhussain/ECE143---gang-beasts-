import streamlit as st 

import streamlit.components.v1 as components


st.title('s')

pdf_path = "../test.pdf"

st.markdown(
    f"""
    <iframe src="{pdf_path}" width="100%" height="700px" style="border:none;"></iframe>
    """,
    unsafe_allow_html=True
)
components.html(
    f"""
    <iframe src="{pdf_path}" width="100%" height="700px" style="border:none;"></iframe>
    """,
    height=700,
)
st.html(
    "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>"
)
