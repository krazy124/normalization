import pandas as pd

"""
raw_df → original uploaded data, untouched
working_df → current active state after applied transformations
preview_df → temporary proposed result before applying
diff_df → rows changed between working and preview
"""


df = pd.read_csv("file.csv")

df = df.apply(lambda col: col.astype(str).str.strip()
              if col.dtype == 'object' else col)
df = df.apply(lambda col: col.astype(str).str.lower()
              if col.dtype == 'object' else col)
