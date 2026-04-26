from turtle import pd

import streamlit as st

st.set_page_config(
    page_title="Data Normalization Assistant",
    page_icon="🧹",
    layout="wide"
)

st.title("Let's Clean Some Data")
st.subheader("Upload messy data, inspect issues, and clean it step by step.")
st.write("A guided data-cleaning assistant for exploring and normalizing CSV files.")


def load_data():
    return pd.read_csv("file.csv")


def strip_whitespace(dataframe):
    return df.apply(lambda col: col.str.strip()
                    if col.dtype == 'object' else col)


def convert_to_lowercase(dataframe):
    return df.apply(lambda col: col.str.lower()
                    if col.dtype == 'object' else col)


def return_duplicates(dataframe):
    return df[df.duplicated()]


def drop_duplicates(dataframe):
    return df.drop_duplicates()


def convert_to_numeric(dataframe, column_name):
    dataframe[column_name] = pd.to_numeric(
        dataframe[column_name], errors="coerce")
    return dataframe
