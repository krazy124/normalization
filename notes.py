import pandas as pd

"""
raw_df → original uploaded data, untouched
working_df → current active state after applied transformations
preview_df → temporary proposed result before applying
diff_df → rows changed between working and preview
"""

# import csv file into pandas dataframe
df = pd.read_csv("file.csv")

# strip whitespace
df = df.apply(lambda col: col.astype(str).str.strip()
              if col.dtype == 'object' else col)
# lowercase all text
df = df.apply(lambda col: col.astype(str).str.lower()
              if col.dtype == 'object' else col)
# identify duplicate rows
duplicate_rows = df[df.duplicated()]
# drop duplicate rows and return cleaned dataframe
df = df.drop_duplicates()
# identify duplicate rows , then drop them and return cleaned dataframe
duplicate_rows = df[df.duplicated()]
df = df.drop_duplicates()
