import streamlit as st

st.set_page_config(
    page_title="Data Normalization Assistant",
    page_icon="🧹",
    layout="wide"
)

st.title("Let's Clean Some Data")
st.subheader("Upload messy data, inspect issues, and clean it step by step.")
st.write("A guided data-cleaning assistant for exploring and normalizing CSV files.")
