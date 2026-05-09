def prepare_column_transformation(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)
    original = df[column_name].copy()

    return df, mask_df, original


def update_column_mask(mask_df, column_name, missing_mask, valid_mask, cleaned_mask, invalid_mask):
    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return mask_df


def convert_to_int_keep_failed(dataframe, column_name, mask_df=None):

    df, mask_df, original = prepare_column_transformation(
        dataframe, column_name, mask_df)

    cleaned = original.astype("string").str.strip()
    converted = pd.to_numeric(cleaned, errors="coerce")

    integer_mask = converted.notna() & (converted % 1 == 0)

    result = original.astype("object").copy()

    result.loc[integer_mask] = converted.loc[integer_mask].astype("Int64")

    df[column_name] = result

    missing_mask = original.isna() | cleaned.eq("")

    valid_mask = original.notna() & ~missing_mask & integer_mask

    cleaned_mask = valid_mask & (
        (cleaned != df[column_name].astype(str))
        | (original.map(type) != df[column_name].map(type))
    )

    invalid_mask = original.notna() & ~missing_mask & ~integer_mask

    mask_df = update_column_mask(
        mask_df, column_name, missing_mask, valid_mask, cleaned_mask, invalid_mask)

    return df, mask_df
