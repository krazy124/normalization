"""Streamlit app for the Data Normalization Assistant."""
"""

Collapse this section when not in use to keep the file easier to scan.
Use as a quick reference for available app utilities.

DATAFRAME-LEVEL FUNCTIONS
+-------------------------------------------+-----------------------------------------------+
| Function Name                             | Parameters                                    |
+-------------------------------------------+-----------------------------------------------+
| load_data                                 | file                                          |
| strip_whitespace                          | dataframe                                     |
| convert_to_lowercase                      | dataframe                                     |
| return_duplicates                         | dataframe                                     |
| drop_duplicates                           | dataframe                                     |
| count_missing_values                      | dataframe                                     |
| return_missing_mask                       | dataframe                                     |
| return_rows_with_missing_values           | dataframe                                     |
| fill_missing_values                       | dataframe, fill_value="Unknown"               |
| get_row_count                             | dataframe                                     |
| get_column_count                          | dataframe                                     |
| count_duplicate_rows                      | dataframe                                     |
| count_total_missing_values                | dataframe                                     |
| get_missing_values_by_column              | dataframe                                     |
| get_missing_row_percent                   | dataframe                                     |
| get_data_health_summary                   | dataframe                                     |
+-------------------------------------------+-----------------------------------------------+

COLUMN-LEVEL FUNCTIONS
+-------------------------------------------+-----------------------------------------------+
| Function Name                             | Parameters                                    |
+-------------------------------------------+-----------------------------------------------+
| convert_col_to_numeric                    | dataframe, column_name                        |
| return_failed_numeric_conversions         | dataframe, column_name                        |
| convert_keep_failed_numeric_conversions   | dataframe, column_name                        |
| convert_to_int_with_na                    | dataframe, column_name                        |
| convert_col_to_datetime                   | dataframe, column_name                        |
| return_failed_datetime_conversions        | dataframe, column_name                        |
| convert_keep_failed_datetime_conversions  | dataframe, column_name                        |
| count_missing_values_in_column            | dataframe, column_name                        |
| return_rows_with_missing_values_in_column | dataframe, column_name                        |
| fill_missing_values_in_column             | dataframe, column_name, fill_value="Unknown"  |
| preview_fill_missing_values_in_column     | dataframe, column_name, fill_value="Unknown"  |
| flag_missing_values_in_column             | dataframe, column_name                        |
+-------------------------------------------+-----------------------------------------------+
"""

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Data Normalization Assistant",
    page_icon="🧹",
    layout="wide"
)

st.title("Let's Clean Some Data")
st.subheader("Upload messy data, inspect issues, and clean it step by step.")
st.write("A guided data-cleaning assistant for exploring and normalizing CSV files.")


# Load Data
def load_data(file):
    return pd.read_csv(file)


# Strip White Space
def strip_whitespace(dataframe):
    return dataframe.apply(
        lambda col: col.str.strip() if col.dtype == "object" else col
    )


# Convert to Lowercase
def convert_to_lowercase(dataframe):
    return dataframe.apply(
        lambda col: col.str.lower() if col.dtype == "object" else col
    )


# Detect and Remove Duplicates
def return_duplicates(dataframe):
    return dataframe[dataframe.duplicated()]


def drop_duplicates(dataframe):
    return dataframe.drop_duplicates()


# Convert to Numeric
def convert_col_to_numeric(dataframe, column_name):
    dataframe = dataframe.copy()
    dataframe[column_name] = pd.to_numeric(
        dataframe[column_name],
        errors="coerce"
    )
    return dataframe


def return_failed_numeric_conversions(dataframe, column_name):
    converted = pd.to_numeric(dataframe[column_name], errors="coerce")
    return dataframe[converted.isna() & dataframe[column_name].notna()]


def convert_keep_failed_numeric_conversions(dataframe, column_name):
    dataframe = dataframe.copy()
    converted = pd.to_numeric(dataframe[column_name], errors="coerce")

    dataframe[column_name] = converted.where(
        converted.notna(),
        dataframe[column_name]
    )
    return dataframe


def convert_to_int_with_na(dataframe, column_name):
    dataframe = dataframe.copy()
    dataframe[column_name] = pd.to_numeric(
        dataframe[column_name],
        errors="coerce"
    ).astype("Int64")
    return dataframe


# Convert to Datetime
def convert_col_to_datetime(dataframe, column_name):
    dataframe = dataframe.copy()
    dataframe[column_name] = pd.to_datetime(
        dataframe[column_name],
        errors="coerce"
    )
    return dataframe


def return_failed_datetime_conversions(dataframe, column_name):
    converted = pd.to_datetime(dataframe[column_name], errors="coerce")
    return dataframe[converted.isna() & dataframe[column_name].notna()]


def convert_keep_failed_datetime_conversions(dataframe, column_name):
    dataframe = dataframe.copy()
    converted = pd.to_datetime(dataframe[column_name], errors="coerce")

    dataframe[column_name] = converted.where(
        converted.notna(),
        dataframe[column_name]
    )
    return dataframe


# =========================
# Missing Values
# =========================

def count_missing_values(dataframe):
    return dataframe.isna().sum()


def return_missing_mask(dataframe):
    return dataframe.isna()


def return_rows_with_missing_values(dataframe):
    return dataframe[dataframe.isna().any(axis=1)]


def fill_missing_values(dataframe, fill_value="Unknown"):
    return dataframe.fillna(fill_value)


def count_missing_values_in_column(dataframe, column_name):
    return dataframe[column_name].isna().sum()


def return_rows_with_missing_values_in_column(dataframe, column_name):
    return dataframe[dataframe[column_name].isna()]


def fill_missing_values_in_column(dataframe, column_name, fill_value="Unknown"):
    dataframe = dataframe.copy()
    dataframe[column_name] = dataframe[column_name].fillna(fill_value)
    return dataframe


def preview_fill_missing_values_in_column(
    dataframe,
    column_name,
    fill_value="Unknown"
):
    preview_dataframe = dataframe.copy()

    before_missing = dataframe[column_name].isna().sum()

    preview_dataframe[column_name] = preview_dataframe[column_name].fillna(
        fill_value
    )

    after_missing = preview_dataframe[column_name].isna().sum()

    return preview_dataframe, before_missing, after_missing


def flag_missing_values_in_column(dataframe, column_name):
    dataframe = dataframe.copy()
    flag_column_name = f"{column_name}_missing_flag"
    dataframe[flag_column_name] = dataframe[column_name].isna()
    return dataframe


# =========================
# Data Health Summary
# =========================

def get_row_count(dataframe):
    return len(dataframe)


def get_column_count(dataframe):
    return len(dataframe.columns)


def count_duplicate_rows(dataframe):
    return dataframe.duplicated().sum()


def count_total_missing_values(dataframe):
    return dataframe.isna().sum().sum()


def get_missing_values_by_column(dataframe):
    return dataframe.isna().sum()


def get_missing_row_percent(dataframe):
    rows_with_missing = dataframe[dataframe.isna().any(axis=1)]

    if len(dataframe) == 0:
        return 0

    return len(rows_with_missing) / len(dataframe) * 100


def get_data_health_summary(dataframe):
    return {
        "row_count": get_row_count(dataframe),
        "column_count": get_column_count(dataframe),
        "duplicate_count": count_duplicate_rows(dataframe),
        "total_missing": count_total_missing_values(dataframe),
        "missing_by_column": get_missing_values_by_column(dataframe),
        "missing_row_percent": get_missing_row_percent(dataframe),
    }
