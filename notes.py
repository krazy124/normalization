import pandas as pd

"""
raw_df → original uploaded data, untouched
working_df → current active state after applied transformations
preview_df → temporary proposed result before applying
diff_df → rows changed between working and preview
"""


# import csv file into pandas dataframe
df = pd.read_csv("file.csv")

# =========================
# Strip White Space
# =========================

df = df.apply(lambda col: col.str.strip()
              if col.dtype == 'object' else col)

# =========================
# Convert to Lowercase
# =========================
df = df.apply(lambda col: col.str.lower()
              if col.dtype == 'object' else col)

# =========================
# Detect and Remove Duplicates
# =========================
# identify duplicate rows
duplicate_rows = df[df.duplicated()]
# drop duplicate rows and return cleaned dataframe
df = df.drop_duplicates()
# identify duplicate rows , then drop them and return cleaned dataframe
duplicate_rows = df[df.duplicated()]
df = df.drop_duplicates()


# =========================
# Convert to Numeric
# =========================
# Convert price column to numeric, coercing errors to NaN
df["price"] = pd.to_numeric(df["price"], errors="coerce")
# Identify rows where conversion failed (original value is not NaN but converted value is NaN)
converted = pd.to_numeric(df["price"], errors="coerce")
failed_rows = df[converted.isna() & df["price"].notna()]
# For rows where conversion failed, keep original value; otherwise, keep converted numeric value
converted = pd.to_numeric(df["price"], errors="coerce")
df["price"] = converted.where(
    converted.notna(),
    df["price"]
)
# Alternatively, if you want to convert to Int64 and keep NaN for failed conversions:
df["price"] = pd.to_numeric(df["price"], errors="coerce").astype("Int64")

# =========================
# Convert to Datetime
# =========================
# Convert order_date column to datetime, coercing errors to NaT
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
# Identify rows where conversion failed (original value is not NaN but converted value is NaT)
converted = pd.to_datetime(df["order_date"], errors="coerce")
failed_rows = df[converted.isna() & df["order_date"].notna()]
# For rows where conversion failed, keep original value; otherwise, keep converted datetime value
converted = pd.to_datetime(df["order_date"], errors="coerce")
df["order_date"] = converted.where(
    converted.notna(),
    df["order_date"]
)

# =========================
# Missing Values
# =========================

# ====== entire dataframe =======

# Counts missing values in every column
missing_counts = df.isna().sum()
# Returns a boolean dataframe indicating where values are missing
missing_mask = df.isna()
# Identify rows with missing values in any column
missing_rows = df[df.isna().any(axis=1)]
# Replace missing values across the entire dataframe with "Unknown"
df = df.fillna("Unknown")

# ====== per column =======
# Count missing values in column_name
missing_count = df["column_name"].isna().sum()
# Identify rows with missing values in column_name
missing_rows = df[df["column_name"].isna()]

# ======= Preview Changes =======
# Create a preview dataframe to show proposed changes without
# modifying the original working dataframe
preview_df = df.copy()

# Count missing values before filling
before_missing = df["column_name"].isna().sum()

# Fill missing values in column_name of the preview dataframe with
# "Unknown" for review before applying to the working dataframe
preview_df["column_name"] = preview_df["column_name"].fillna("Unknown")

# Count missing values after filling in the preview dataframe
after_missing = preview_df["column_name"].isna().sum()


# ======= Apply Changes =======
# Fill missing values in column_name after preview/review
df["column_name"] = df["column_name"].fillna("Unknown")
# Alternatively, create a new column to flag missing values instead of filling them
df["category_missing_flag"] = df["category"].isna()


# =========================
# Data Health Summary
# =========================

# Total rows and columns
row_count = len(df)
column_count = len(df.columns)

# Count duplicate rows
duplicate_count = df.duplicated().sum()

# Count total missing values
total_missing = df.isna().sum().sum()

# Missing values by column
missing_by_column = df.isna().sum()

# Percent of rows with at least one missing value
rows_with_missing = df[df.isna().any(axis=1)]
missing_row_percent = len(rows_with_missing) / len(df) * 100
