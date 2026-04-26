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
