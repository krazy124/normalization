# F7v1
def get_missing_values_by_column(dataframe):
    return dataframe.isna().sum()


# F15v2
def fill_missing_values(dataframe, fill_value="Unknown", mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    missing_mask_df = df.isna()

    df = df.fillna(fill_value)

    for column_name in df.columns:
        mask_df.loc[missing_mask_df[column_name], column_name] = "cleaned"
        mask_df.loc[~missing_mask_df[column_name], column_name] = "valid"

    return df, mask_df


# F16v1
def count_missing_values(dataframe):
    return dataframe.isna().sum()


# F20v1
def count_missing_values_in_column(dataframe, column_name):
    return dataframe[column_name].isna().sum()


# F21v1
def return_rows_with_missing_values_in_column(dataframe, column_name):
    return dataframe[dataframe[column_name].isna()]


# F23v1
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


# F24v2
def flag_missing_values_in_column(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    flag_column_name = f"{column_name}_missing_flag"
    df[flag_column_name] = df[column_name].isna()

    mask_df = create_or_update_transformation_mask(df, mask_df)

    mask_df.loc[df[column_name].isna(), column_name] = "missing"
    mask_df.loc[df[column_name].notna(), column_name] = "valid"
    mask_df[flag_column_name] = "cleaned"

    return df, mask_df


# F26v2
def convert_keep_failed_numeric_conversions(dataframe, column_name, mask_df=None):
    return convert_col_to_numeric(dataframe, column_name, mask_df)


# F27v2
def convert_to_int_with_na(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    converted = pd.to_numeric(original, errors="coerce")

    df[column_name] = converted.astype("Int64")

    missing_mask = original.isna()
    valid_mask = original.notna() & converted.notna()
    cleaned_mask = valid_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    invalid_mask = original.notna() & converted.isna()

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F28v1
def return_failed_numeric_conversions(dataframe, column_name):
    converted = pd.to_numeric(dataframe[column_name], errors="coerce")
    return dataframe[converted.isna() & dataframe[column_name].notna()]


# F29v2
def convert_col_to_datetime(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    converted = pd.to_datetime(original, errors="coerce")

    df[column_name] = converted

    missing_mask = original.isna()
    valid_mask = original.notna() & converted.notna()
    cleaned_mask = valid_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    invalid_mask = original.notna() & converted.isna()

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F30v2
def convert_keep_failed_datetime_conversions(dataframe, column_name, mask_df=None):
    return convert_common_date_patterns(dataframe, column_name, mask_df)


# F31v1
def return_failed_datetime_conversions(dataframe, column_name):
    converted = pd.to_datetime(dataframe[column_name], errors="coerce")
    return dataframe[converted.isna() & dataframe[column_name].notna()]


# F38v1
def get_conversion_success_percent(original_df, preview_df, column_name):
    original = original_df[column_name]
    preview = preview_df[column_name]

    non_null_mask = original.notna()
    eligible_rows = non_null_mask.sum()

    if eligible_rows == 0:
        return "0%"

    changed_rows = (
        original.astype(str) != preview.astype(str)
    ) & non_null_mask

    changed_count = changed_rows.sum()

    return f"{(changed_count / eligible_rows) * 100:.0f}%"


# F39v1
def return_failed_clean_type_rows(dataframe, column_name):
    column = dataframe[column_name]

    numeric_converted = pd.to_numeric(column, errors="coerce")
    datetime_converted = pd.to_datetime(column, errors="coerce")

    failed_mask = (
        column.notna()
        & numeric_converted.isna()
        & datetime_converted.isna()
    )

    return dataframe[failed_mask]


# F40v1
def highlight_failed_clean_type_rows(dataframe, column_name):
    column = dataframe[column_name]

    numeric_converted = pd.to_numeric(column, errors="coerce")
    datetime_converted = pd.to_datetime(column, errors="coerce")

    failed_mask = (
        column.notna()
        & numeric_converted.isna()
        & datetime_converted.isna()
    )

    failed_rows = dataframe[failed_mask].copy()

    def highlight_cell(row):
        styles = [""] * len(row)
        col_index = failed_rows.columns.get_loc(column_name)

        if pd.notna(row[column_name]):
            styles[col_index] = (
                "background-color: #5c1f1f; "
                "color: #ffffff; "
                "font-weight: bold;"
            )

        return styles

    return failed_rows.style.apply(highlight_cell, axis=1)


# # F49v1
# def generate_transformation_code(transformation_steps):
#     code_lines = [
#         "def clean_data(df):",
#         "    mask_df = create_or_update_transformation_mask(df)",
#         ""
#     ]

#     for step in transformation_steps:
#         function_name = step["function"]
#         column_name = step["column"]

#         code_lines.append(
#             f'    df, mask_df = {function_name}(df, "{column_name}", mask_df)'
#         )

#     code_lines.extend([
#         "",
#         "    return df, mask_df"
#     ])

#     return "\n".join(code_lines)
