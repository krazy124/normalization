import random
import pandas as pd
import streamlit as st
import base64
import re
from pathlib import Path


# F1v1
def create_or_update_transformation_mask(dataframe, mask_df=None):
    if mask_df is None:
        mask_df = pd.DataFrame(
            "unprocessed",
            index=dataframe.index,
            columns=dataframe.columns
        )
    else:
        mask_df = mask_df.copy()

    mask_df = mask_df.reindex(index=dataframe.index)

    for column_name in dataframe.columns:
        if column_name not in mask_df.columns:
            mask_df[column_name] = "unprocessed"

        missing_mask = (
            dataframe[column_name].isna()
            | dataframe[column_name].astype(str).str.strip().eq("")
        )

        mask_df.loc[missing_mask, column_name] = "missing"

    return mask_df[dataframe.columns]


# F2v1
def generate_dirty_data(record_count):
    random.seed(42)

    first_names = [
        " John", "jane ", "ALICE", "bob", " Charlie ", "dAvE", " Eve",
        "frank ", "GRACE", " hannah", "Isaac ", "JULIA", " kevin"
    ]

    last_names = [
        " Smith", "johnson ", "WILLIAMS", "brown", " Jones ",
        "Miller", " Davis", "garcia ", "RODRIGUEZ", "wilson "
    ]

    cities = [
        " New York", "los angeles ", "CHICAGO", "houston",
        " Phoenix ", "SAN ANTONIO ", " Dallas ", "austin"
    ]

    departments = [
        " Sales", "engineering ", "HR", "marketing", " Finance ",
        "operations", "IT ", "support"
    ]

    statuses = [
        "Active", " inactive ", "PENDING", "active ", " Suspended", None
    ]

    notes = [
        " good client", "Needs Follow Up ", "VIP", " late payer ",
        "Returned item", None, "duplicate?", "  ", "Prefers email"
    ]

    dirty_numbers = [
        "100", " 250 ", "$300", "N/A", "four hundred",
        None, "500.00", " 75", "1,200", "??"
    ]

    dirty_dates = [
        "2024-01-15", "01/22/2024", "March 5 2024",
        "2024/04/18", "not a date", None, "13/13/2024",
        "2024-07-32", " 2024-09-10 ", "02-28-2024"
    ]

    emails = [
        "test@example.com", " USER@MAIL.COM ", "bademail@",
        "none", None, "sample.user@gmail.com", "hello@site",
        "foo@bar.com "
    ]

    scores = ["90", "85 ", " seventy", None, "100", "N/A", " 72"]

    rows = []

    for i in range(record_count):
        row = {
            "customer_id": random.choice([i + 1, i + 1, i, None]),
            "full_name": (
                f"{random.choice(first_names)} {random.choice(last_names)}"
            ),
            "email": random.choice(emails),
            "city": random.choice(cities),
            "department": random.choice(departments),
            "status": random.choice(statuses),
            "purchase_amount": random.choice(dirty_numbers),
            "signup_date": random.choice(dirty_dates),
            "notes": random.choice(notes),
            "score": random.choice(scores),
        }

        rows.append(row)

    if record_count > 25:
        rows[10] = rows[5].copy()
        rows[25] = rows[5].copy()

    if record_count > 75:
        rows[50] = rows[20].copy()
        rows[75] = rows[20].copy()

    return pd.DataFrame(rows)


# F3v1
def get_row_count(dataframe):
    return len(dataframe)


# F4v1
def get_column_count(dataframe):
    return len(dataframe.columns)


# F5v1
def count_duplicate_rows(dataframe):
    return dataframe.duplicated().sum()


# F6v1
def count_total_missing_values(dataframe):
    return dataframe.isna().sum().sum()


# F7v1
def count_rows_with_missing_values(dataframe):
    return dataframe.isna().any(axis=1).sum()


# F8v1
def get_missing_percent_by_column(dataframe):
    if len(dataframe) == 0:
        return pd.Series(0, index=dataframe.columns)

    return (dataframe.isna().sum() / len(dataframe)) * 100


# F9v1
def get_missing_row_percent(dataframe):
    rows_with_missing = dataframe[dataframe.isna().any(axis=1)]

    if len(dataframe) == 0:
        return 0

    return len(rows_with_missing) / len(dataframe) * 100


# F10v1
def get_data_health_summary(dataframe):
    return {
        "row_count": get_row_count(dataframe),
        "column_count": get_column_count(dataframe),
        "duplicate_count": count_duplicate_rows(dataframe),
        "total_missing": count_total_missing_values(dataframe),
        "rows_with_missing": count_rows_with_missing_values(dataframe),
        "missing_by_column": get_missing_percent_by_column(dataframe),
        "missing_row_percent": get_missing_row_percent(dataframe),
    }


# F11v1
def get_column_health(dataframe, column_name):
    column = dataframe[column_name]
    total_rows = len(column)
    non_missing_count = column.notna().sum()

    if total_rows == 0:
        return {
            "Missing %": "0%",
            "Unique Count": 0,
            "Duplicate Count": 0,
            "Best Detected Type": "Unknown",
            "Valid Type %": "0%",
            "Invalid / Unclean Count": 0,
        }

    missing_percent = column.isna().sum() / total_rows * 100
    unique_count = column.nunique(dropna=True)
    duplicate_count = column.duplicated().sum()

    if non_missing_count == 0:
        return {
            "Missing %": f"{missing_percent:.0f}%",
            "Unique Count": unique_count,
            "Duplicate Count": duplicate_count,
            "Best Detected Type": "Missing",
            "Valid Type %": "0%",
            "Invalid / Unclean Count": 0,
        }

    numeric_converted = pd.to_numeric(column, errors="coerce")
    datetime_converted = pd.to_datetime(column, errors="coerce")

    numeric_valid_count = numeric_converted.notna().sum()
    datetime_valid_count = datetime_converted.notna().sum()

    numeric_valid_percent = numeric_valid_count / non_missing_count * 100
    datetime_valid_percent = datetime_valid_count / non_missing_count * 100

    if numeric_valid_percent >= datetime_valid_percent:
        best_detected_type = "Numeric"
        valid_type_percent = numeric_valid_percent
        invalid_unclean_count = non_missing_count - numeric_valid_count
    else:
        best_detected_type = "Datetime"
        valid_type_percent = datetime_valid_percent
        invalid_unclean_count = non_missing_count - datetime_valid_count

    return {
        "Missing %": f"{missing_percent:.0f}%",
        "Unique Count": unique_count,
        "Duplicate Count": duplicate_count,
        "Best Detected Type": best_detected_type,
        "Valid Type %": f"{valid_type_percent:.0f}%",
        "Invalid / Unclean Count": invalid_unclean_count,
    }


class Transformation:
    @staticmethod
    def to_int_keep_failed(series):
        original = series.copy()
        cleaned = original.astype("string").str.strip()
        converted = pd.to_numeric(cleaned, errors="coerce")
        integer_mask = converted.notna() & (converted % 1 == 0)

        result = original.astype("object").copy()
        result.loc[integer_mask] = converted.loc[integer_mask].astype("Int64")
        return result

    @staticmethod
    def common_date_patterns(series):
        original = series.copy()
        cleaned = original.astype("string").str.strip()
        converted = pd.to_datetime(cleaned, errors="coerce")

        result = original.astype("object").copy()
        result.loc[converted.notna()] = converted.loc[converted.notna()]
        return result

    @staticmethod
    def clean_validate_email(series):
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        original = series.copy()

        cleaned = (
            original
            .astype("string")
            .str.strip()
            .str.lower()
            .str.replace(r"\s+", "", regex=True)
        )

        junk_values = ["", "na", "n/a", "none", "null", "nan"]
        cleaned = cleaned.mask(cleaned.isin(junk_values), pd.NA)

        valid_email_mask = cleaned.str.match(email_pattern, na=False)

        return cleaned.where(
            valid_email_mask | cleaned.isna(),
            original
        )

    @staticmethod
    def currency_to_numeric(series):
        original = series.copy()

        cleaned = (
            original
            .astype("string")
            .str.replace(r"[\$,]", "", regex=True)
            .str.strip()
        )

        converted = pd.to_numeric(cleaned, errors="coerce")

        result = original.astype("object").copy()
        result.loc[converted.notna()] = converted.loc[converted.notna()]
        return result


# F12v1
def strip_whitespace(dataframe, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    for column_name in df.columns:
        if df[column_name].dtype == "object" or pd.api.types.is_string_dtype(df[column_name]):
            df[column_name] = df[column_name].map(
                lambda value: value.strip() if isinstance(value, str) else value
            )

    return df, mask_df


# F13v1
def convert_to_lowercase(dataframe, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    for column_name in df.columns:
        if df[column_name].dtype == "object" or pd.api.types.is_string_dtype(df[column_name]):
            df[column_name] = df[column_name].map(
                lambda value: value.lower() if isinstance(value, str) else value
            )

    return df, mask_df


# F14v1
def drop_duplicates(dataframe, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    df = df.drop_duplicates()
    mask_df = mask_df.reindex(index=df.index)

    return df, mask_df


# F17v1
def fill_missing_values_in_column(
    dataframe,
    column_name,
    fill_value="Unknown",
    mask_df=None
):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    missing_mask = original.isna()
    valid_mask = original.notna()

    df[column_name] = df[column_name].fillna(fill_value)

    mask_df.loc[missing_mask, column_name] = "cleaned"
    mask_df.loc[valid_mask, column_name] = "valid"

    return df, mask_df


# F21v1
def convert_iso_date_pattern(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = original.astype(str).str.strip()
    pattern_mask = cleaned.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)

    converted = pd.to_datetime(
        cleaned[pattern_mask],
        format="%Y-%m-%d",
        errors="coerce"
    )

    valid_pattern_mask = pattern_mask.copy()
    valid_pattern_mask.loc[pattern_mask] = converted.notna()

    df.loc[valid_pattern_mask, column_name] = converted[converted.notna()]

    missing_mask = original.isna()
    cleaned_mask = valid_pattern_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    valid_mask = valid_pattern_mask & ~cleaned_mask
    invalid_mask = pattern_mask & ~valid_pattern_mask

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F22v1
def convert_us_dash_date_pattern(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = original.astype(str).str.strip()
    pattern_mask = cleaned.str.match(r"^\d{2}-\d{2}-\d{4}$", na=False)

    converted = pd.to_datetime(
        cleaned[pattern_mask],
        format="%m-%d-%Y",
        errors="coerce"
    )

    valid_pattern_mask = pattern_mask.copy()
    valid_pattern_mask.loc[pattern_mask] = converted.notna()

    df.loc[valid_pattern_mask, column_name] = converted[converted.notna()]

    missing_mask = original.isna()
    cleaned_mask = valid_pattern_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    valid_mask = valid_pattern_mask & ~cleaned_mask
    invalid_mask = pattern_mask & ~valid_pattern_mask

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F23v1
def convert_us_slash_date_pattern(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = original.astype(str).str.strip()
    pattern_mask = cleaned.str.match(r"^\d{2}/\d{2}/\d{4}$", na=False)

    converted = pd.to_datetime(
        cleaned[pattern_mask],
        format="%m/%d/%Y",
        errors="coerce"
    )

    valid_pattern_mask = pattern_mask.copy()
    valid_pattern_mask.loc[pattern_mask] = converted.notna()

    df.loc[valid_pattern_mask, column_name] = converted[converted.notna()]

    missing_mask = original.isna()
    cleaned_mask = valid_pattern_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    valid_mask = valid_pattern_mask & ~cleaned_mask
    invalid_mask = pattern_mask & ~valid_pattern_mask

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F24v1
def convert_text_month_date_pattern(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = original.astype(str).str.strip().str.lower()
    pattern_mask = cleaned.str.match(
        r"^[a-zA-Z]+\s+\d{1,2}\s+\d{4}$",
        na=False
    )

    converted = pd.to_datetime(
        cleaned[pattern_mask],
        format="%B %d %Y",
        errors="coerce"
    )

    valid_pattern_mask = pattern_mask.copy()
    valid_pattern_mask.loc[pattern_mask] = converted.notna()

    df.loc[valid_pattern_mask, column_name] = converted[converted.notna()]

    missing_mask = original.isna()
    cleaned_mask = valid_pattern_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    valid_mask = valid_pattern_mask & ~cleaned_mask
    invalid_mask = pattern_mask & ~valid_pattern_mask

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F25v1
def convert_iso_slash_date_pattern(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = original.astype(str).str.strip()
    pattern_mask = cleaned.str.match(r"^\d{4}/\d{2}/\d{2}$", na=False)

    converted = pd.to_datetime(
        cleaned[pattern_mask],
        format="%Y/%m/%d",
        errors="coerce"
    )

    valid_pattern_mask = pattern_mask.copy()
    valid_pattern_mask.loc[pattern_mask] = converted.notna()

    df.loc[valid_pattern_mask, column_name] = converted[converted.notna()]

    missing_mask = original.isna()
    cleaned_mask = valid_pattern_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    valid_mask = valid_pattern_mask & ~cleaned_mask
    invalid_mask = pattern_mask & ~valid_pattern_mask

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F26v1
def convert_common_date_patterns(dataframe, column_name, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()

    df, mask_df = convert_iso_date_pattern(df, column_name, mask_df)
    df, mask_df = convert_us_dash_date_pattern(df, column_name, mask_df)
    df, mask_df = convert_us_slash_date_pattern(df, column_name, mask_df)
    df, mask_df = convert_text_month_date_pattern(df, column_name, mask_df)
    df, mask_df = convert_iso_slash_date_pattern(df, column_name, mask_df)

    final_converted = pd.to_datetime(df[column_name], errors="coerce")

    missing_mask = original.isna()
    valid_or_cleaned_mask = original.notna() & final_converted.notna()
    cleaned_mask = valid_or_cleaned_mask & (
        original.astype(str) != df[column_name].astype(str)
    )
    valid_mask = valid_or_cleaned_mask & ~cleaned_mask
    invalid_mask = original.notna() & final_converted.isna()

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df

# =========================
# Email Cleaning / Validation
# =========================


# F27.1v2
def run_column_transformation(dataframe, column_name, transformation_function, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    transformed = transformation_function(original)

    df[column_name] = transformed

    missing_mask = original.isna() | original.astype(str).str.strip().eq("")

    cleaned_mask = (
        ~missing_mask
        & (original.astype(str) != transformed.astype(str))
    )

    valid_mask = ~missing_mask & ~cleaned_mask

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"

    return df, mask_df


# F27.1v1
def run_string_transformation(dataframe, column_name, transformation_function, mask_df=None):

    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)
    original = df[column_name].copy()

    if (original.dtype == "object" or pd.api.types.is_string_dtype(original)):

        transformed = original.map(lambda value: transformation_function(
            value)if isinstance(value, str)else value)
        df[column_name] = transformed
        missing_mask = original.isna()
        cleaned_mask = (original.notna() & original.map(lambda value: isinstance(
            value, str)) & (original.astype(str) != transformed.astype(str)))

        valid_mask = (original.notna() & ~cleaned_mask)
        mask_df.loc[missing_mask, column_name] = "missing"
        mask_df.loc[valid_mask, column_name] = "valid"
        mask_df.loc[cleaned_mask, column_name] = "cleaned"

    return df, mask_df


# =========================
# Preview / Compare Helpers
# =========================


# F28v1
def sort_transformation_preview(compare_df, original_column, preview_column):
    sorted_df = compare_df.copy()

    def get_sort_group(row):
        original_value = row[original_column]
        preview_value = row[preview_column]

        original_missing = pd.isna(original_value) or str(
            original_value).strip() == ""
        preview_missing = pd.isna(preview_value) or str(
            preview_value).strip() == ""

        if original_missing and preview_missing:
            return 2

        if str(original_value) == str(preview_value):
            return 0

        return 1

    sorted_df["_sort_group"] = sorted_df.apply(get_sort_group, axis=1)

    sorted_df = sorted_df.sort_values(
        by="_sort_group",
        ascending=True
    )

    return sorted_df.drop(columns=["_sort_group"])

# =========================
# Reports / Diagnostics
# =========================


# F29v1
def return_transformation_mask(mask_df):
    return mask_df.copy()


# F30v1
def return_rows_with_missing_values(dataframe):
    return dataframe[dataframe.isna().any(axis=1)]


# F31v1
def return_duplicates(dataframe):
    return dataframe[dataframe.duplicated()]


# F32v1
def return_invalid_format_report(dataframe, mask_df):
    report_rows = []

    for column_name in mask_df.columns:
        invalid_rows = mask_df[column_name] == "invalid format"

        for index in dataframe[invalid_rows].index:
            value = dataframe.loc[index, column_name]

            reason = get_invalid_format_reason(
                column_name,
                value
            )

            report_rows.append({
                "Row Index": index,
                "Column": column_name,
                "Value": value,
                "Reason": reason
            })

    return pd.DataFrame(report_rows)

# =========================
# Invalid Format Reason Helpers
# =========================


# F33v1
def get_invalid_format_reason(column_name, value):
    column_lower = column_name.lower()

    if "email" in column_lower:
        return get_email_invalid_reason(value)

    if "date" in column_lower:
        return get_datetime_invalid_reason(value)

    if "amount" in column_lower or "price" in column_lower:
        return get_currency_invalid_reason(value)

    return "Invalid format"


# F34v1
def get_email_invalid_reason(value):
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if pd.isna(value):
        return "Missing email"

    value = str(value).strip().lower().replace(" ", "")

    if value in ["", "na", "n/a", "none", "null", "nan"]:
        return "Missing email"

    if value.count("@") == 0:
        return "Missing @ symbol"

    if value.count("@") > 1:
        return "More than one @ symbol"

    local, domain = value.split("@")

    if local == "":
        return "Missing name before @"

    if domain == "":
        return "Missing domain after @"

    if "." not in domain:
        return "Missing domain extension"

    if domain.startswith("."):
        return "Domain starts with dot"

    if domain.endswith("."):
        return "Domain ends with dot"

    if not re.match(email_pattern, value):
        return "Invalid email format"

    return "Invalid format"


# F35v1
def get_datetime_invalid_reason(value):
    if pd.isna(value):
        return "Missing date"

    value = str(value).strip()

    if value == "":
        return "Missing date"

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.notna(parsed):
        return "Invalid format"

    if any(char.isalpha() for char in value):
        return "Unrecognized date text"

    if value.count("/") == 2 or value.count("-") == 2:
        parts = re.split(r"[-/]", value)

        if len(parts) == 3:
            try:
                nums = [int(part) for part in parts]

                if len(parts[0]) == 4:
                    year, month, day = nums
                else:
                    month, day, year = nums

                if month < 1 or month > 12:
                    return "Invalid month"

                if day < 1 or day > 31:
                    return "Invalid day"

            except ValueError:
                return "Invalid date format"

    return "Unrecognized date format"


# F36v1
def get_currency_invalid_reason(value):
    if pd.isna(value):
        return "Missing currency value"

    value = str(value).strip()

    if value == "":
        return "Missing currency value"

    cleaned = re.sub(r"[\$,]", "", value)

    converted = pd.to_numeric(cleaned, errors="coerce")

    if pd.notna(converted):
        return "Invalid format"

    if any(char.isalpha() for char in value):
        return "Contains text"

    if "?" in value:
        return "Unknown value"

    return "Invalid currency format"

# =========================
# Transformation Code Generation
# =========================


# F37v1
def add_transformation_step(function_name, column_name):
    if "transformation_steps" not in st.session_state:
        st.session_state.transformation_steps = []

    st.session_state.transformation_steps.append({
        "function": function_name,
        "column": column_name
    })


# F38v1
def generate_transformation_code(transformation_steps):
    code_lines = [
        "import pandas as pd",
        "",
        "",
        "def clean_data(df):",
        "    df = df.copy()",
        ""
    ]

    for step in transformation_steps:
        code_lines.append(
            get_pure_transformation_code(
                step["function"],
                step["column"]
            )
        )

    code_lines.extend([
        "",
        "    return df"
    ])

    return "\n".join(code_lines)


# F39v1
def get_pure_transformation_code(function_name, column_name):
    templates = {
        "convert_col_to_numeric": f'''
    # Convert to Float: {column_name}
    converted = pd.to_numeric(df["{column_name}"], errors="coerce")

    df["{column_name}"] = converted.where(
        converted.notna(),
        df["{column_name}"]
    )
''',

        "convert_to_int_keep_failed": f'''
    # Convert to Int: {column_name}
    cleaned = df["{column_name}"].astype("string").str.strip()
    converted = pd.to_numeric(cleaned, errors="coerce")

    integer_mask = converted.notna() & (converted % 1 == 0)

    result = df["{column_name}"].astype("object").copy()
    result.loc[integer_mask] = converted.loc[integer_mask].astype("Int64")

    df["{column_name}"] = result
''',

        "convert_common_date_patterns": f'''
    # Convert to Datetime: {column_name}
    cleaned = df["{column_name}"].astype("string").str.strip()
    converted = pd.to_datetime(cleaned, errors="coerce")

    result = df["{column_name}"].astype("object").copy()
    result.loc[converted.notna()] = converted.loc[converted.notna()]

    df["{column_name}"] = result
''',

        "clean_and_validate_email_column": f'''
    # Clean / Validate Email: {column_name}
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,}}$"

    original = df["{column_name}"].copy()

    cleaned = (
        df["{column_name}"]
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\\s+", "", regex=True)
    )

    junk_values = ["", "na", "n/a", "none", "null", "nan"]
    cleaned = cleaned.mask(cleaned.isin(junk_values), pd.NA)

    valid_email_mask = cleaned.str.match(email_pattern, na=False).fillna(False)

    df["{column_name}"] = cleaned.where(
        valid_email_mask | cleaned.isna(),
        original
    )
''',

        "fill_missing_values_in_column": f'''
    # Fill Missing: {column_name}
    df["{column_name}"] = df["{column_name}"].fillna("Unknown")
''',

        "convert_currency_to_numeric": f'''
    # Convert Currency: {column_name}
    cleaned = (
        df["{column_name}"]
        .astype("string")
        .str.replace(r"[\\$,]", "", regex=True)
        .str.strip()
    )

    converted = pd.to_numeric(cleaned, errors="coerce")

    result = df["{column_name}"].astype("object").copy()
    result.loc[converted.notna()] = converted.loc[converted.notna()]

    df["{column_name}"] = result
''',

        "convert_to_titlecase": f'''
    # Convert to Title Case: {column_name}
    df["{column_name}"] = df["{column_name}"].map(
        lambda value: value.title() if isinstance(value, str) else value
    )
''',

        "convert_column_to_lowercase": f'''
    # Convert to Lowercase: {column_name}
    df["{column_name}"] = df["{column_name}"].map(
        lambda value: value.lower() if isinstance(value, str) else value
    )
'''
    }

    return templates.get(
        function_name,
        f'''
    # Unsupported transformation: {function_name} on {column_name}
'''
    )


# =========================
# S1v1 - Streamlit Page Setup
# =========================
st.set_page_config(
    page_title="Function Test Page",
    page_icon="🧪",
    layout="wide"
)


# =========================
# S2v1 - App Styling
# =========================
image_path = Path("assets/matrix_background.png")
encoded_image = base64.b64encode(image_path.read_bytes()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-color:  rgb(0, 17, 57);
}}

.main .block-container {{
    background: rgb(0, 17, 57);
    border-radius: 14px;
    padding: 2rem;
}}
</style>
""", unsafe_allow_html=True)


# =========================
# S3v1 - Main Title
# =========================
st.title("Function Test Page")


# =========================
# S4v2 - Dirty Data Display Section
# =========================
st.write("### Data Frame Transformation Section")

with st.container(border=True):

    # S4.1v1 - Layout Columns
    left_panel, right_panel = st.columns([1, 6])

    with left_panel:

        # S4.2v1 - Record Count Input
        record_count = st.number_input(
            "Enter number of records",
            min_value=1,
            max_value=1000,
            value=25,
            step=1
        )

        # S4.3v2 - Dirty Data Session State
        if "dirty_df" not in st.session_state:
            st.session_state.dirty_df = generate_dirty_data(record_count)

        if "dirty_mask" not in st.session_state:
            st.session_state.dirty_mask = create_or_update_transformation_mask(
                st.session_state.dirty_df
            )

        if "preview_df" not in st.session_state:
            st.session_state.preview_df = st.session_state.dirty_df.copy()

        if "preview_mask" not in st.session_state:
            st.session_state.preview_mask = st.session_state.dirty_mask.copy()

        if "transformation_steps" not in st.session_state:
            st.session_state.transformation_steps = []

        # S4.4v2 - Generate Data Button
        if st.button("Generate Data", use_container_width=True):
            st.session_state.dirty_df = generate_dirty_data(record_count)
            st.session_state.dirty_mask = create_or_update_transformation_mask(
                st.session_state.dirty_df
            )

            st.session_state.preview_df = st.session_state.dirty_df.copy()
            st.session_state.preview_mask = st.session_state.dirty_mask.copy()

        st.write("")

        # S4.5v2 - DataFrame Transformation Buttons
        if st.button("Strip Whitespace", use_container_width=True):
            st.session_state.dirty_df, st.session_state.dirty_mask = strip_whitespace(
                st.session_state.dirty_df,
                st.session_state.dirty_mask
            )

        if st.button("Convert to Lowercase", use_container_width=True):
            st.session_state.dirty_df, st.session_state.dirty_mask = convert_to_lowercase(
                st.session_state.dirty_df,
                st.session_state.dirty_mask
            )

        if st.button("Drop Duplicates", use_container_width=True):
            st.session_state.dirty_df, st.session_state.dirty_mask = drop_duplicates(
                st.session_state.dirty_df,
                st.session_state.dirty_mask
            )

    with right_panel:

        # S4.6v1 - Dirty DataFrame Display
        st.dataframe(st.session_state.dirty_df, use_container_width=True)


# =========================
# S5v1 - Data Health Dashboard
# =========================
summary = get_data_health_summary(st.session_state.dirty_df)
missing_by_column = summary["missing_by_column"]

with st.container(border=True):

    # S5.1v1 - Dashboard Layout Columns
    left_panel, right_panel = st.columns([1, 2])

with left_panel:
    with st.container(border=True):

        # S5.2v1 - Row Health Metrics
        st.write("#### Row Health")

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric("Rows", summary["row_count"])

        with metric_col2:
            st.metric("Duplicates", summary["duplicate_count"])

        with metric_col3:
            st.metric("Rows w/ Missing", summary["rows_with_missing"])

        with metric_col4:
            st.metric(
                "Incomplete Rows %",
                f"{summary['missing_row_percent']:.0f}%"
            )

with right_panel:
    with st.container(border=True):

        # S5.3v1 - Column Missing Rate Metrics
        st.write("#### Column Missing Rate")

        missing_cols = st.columns(10)
        column_names = list(missing_by_column.index)

        for index, column_name in enumerate(column_names):
            with missing_cols[index % 10]:
                st.metric(
                    column_name,
                    f"{missing_by_column[column_name]:.0f}%"
                )


# =========================
# S6v2 - Column Transformation Preview
# =========================
st.write("### Column Transformations")

with st.container(border=True):

    # S6.1v1 - Column Selector Layout
    left, right = st.columns([2, 3])

    with left:

        # S6.2v1 - Selected Column Dropdown
        selected_column = st.selectbox(
            "Select a column to transform",
            st.session_state.dirty_df.columns
        )

    # S6.3v2 - Preview Session State
    if "preview_df" not in st.session_state:
        st.session_state.preview_df = st.session_state.dirty_df.copy()

    if "preview_mask" not in st.session_state:
        st.session_state.preview_mask = st.session_state.dirty_mask.copy()

    if "last_selected_column" not in st.session_state:
        st.session_state.last_selected_column = selected_column

    if st.session_state.last_selected_column != selected_column:
        st.session_state.preview_df = st.session_state.dirty_df.copy()
        st.session_state.preview_mask = st.session_state.dirty_mask.copy()
        st.session_state.last_selected_column = selected_column

    # S6.4v1 - Column Transformation Layout
    transform_col, blank_col1, compare_col, blank_col2, health_col = st.columns([
        2, 1, 4, 1, 4
    ])

    with transform_col:

        # S6.5v4 - Column Transformation Buttons
        st.write("#### Transformations")
        st.write("")
        st.write("")

        if st.button("Convert to Float", key="col_convert_numeric", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask =
            run_column_transformation(dataframe=st.session_state.preview_df, column_name=selected_column, transformation_function=lambda series: pd.to_numeric(series, errors="coerce").
                                      where(pd.to_numeric(series, errors="coerce").
                                            notna(), series), mask_df=st.session_state.preview_mask)
            add_transformation_step("convert_col_to_numeric", selected_column)

        if st.button("Convert to Int", key="col_convert_int", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=Transformation.to_int_keep_failed,
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step(
                "convert_to_int_keep_failed", selected_column)

        if st.button("Convert to Datetime", key="col_convert_datetime", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=Transformation.common_date_patterns,
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step(
                "convert_common_date_patterns", selected_column)

        if st.button("Clean / Validate Email", key="col_clean_validate_email", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=Transformation.clean_validate_email,
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step(
                "clean_and_validate_email_column", selected_column)

        if st.button("Fill Missing", key="col_fill_missing", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=lambda series: series.fillna(
                    "Unknown"),
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step(
                "fill_missing_values_in_column", selected_column)

        if st.button("Convert Currency", key="col_convert_currency", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=Transformation.currency_to_numeric,
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step(
                "convert_currency_to_numeric", selected_column)

        if st.button("Convert to Title Case", key="col_convert_title", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=lambda series: series.map(
                    lambda value: value.title() if isinstance(value, str) else value
                ),
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step("convert_to_titlecase", selected_column)

        if st.button("Convert to Lowercase", key="col_convert_lowercase", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=lambda series: series.map(
                    lambda value: value.lower() if isinstance(value, str) else value
                ),
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step(
                "convert_column_to_lowercase", selected_column)

        st.write("")

        if st.button("Apply Changes to DataFrame", key="apply_column_preview", use_container_width=True):
            st.session_state.dirty_df = st.session_state.preview_df.copy()
            st.session_state.dirty_mask = st.session_state.preview_mask.copy()

            st.session_state.preview_df = st.session_state.dirty_df.copy()
            st.session_state.preview_mask = st.session_state.dirty_mask.copy()
            st.rerun()

    with compare_col:

        # S6.6v3 - Original vs Preview Compare Table
        st.write(f"#### Original vs Preview: {selected_column}")

        original_column = f"Original: {selected_column}"
        preview_column = f"Preview: {selected_column}"

        compare_df = pd.DataFrame({
            original_column: st.session_state.dirty_df[selected_column],
            preview_column: st.session_state.preview_df[selected_column]
        })

        valid_col = f"{selected_column}_valid"
        reason_col = f"{selected_column}_invalid_reason"

        if (
            valid_col in st.session_state.preview_df.columns
            and reason_col in st.session_state.preview_df.columns
        ):
            compare_df["Valid"] = st.session_state.preview_df[valid_col]
            compare_df["Invalid Reason"] = st.session_state.preview_df[reason_col]

            def get_email_sort_group(row):
                reason = row["Invalid Reason"]
                valid = row["Valid"]

                if reason == "Missing email":
                    return 2

                if valid is True:
                    return 1

                return 0

            compare_df["_sort_group"] = compare_df.apply(
                get_email_sort_group,
                axis=1
            )

            compare_df = compare_df.sort_values(
                by="_sort_group",
                ascending=True
            )

            compare_df = compare_df.drop(columns=["_sort_group"])

        else:
            compare_df = sort_transformation_preview(
                compare_df,
                original_column,
                preview_column
            )

        st.dataframe(compare_df, use_container_width=True, height=550)

    with health_col:

        # S6.7v1 - Column Health Preview
        st.write("#### Column Health Preview")

        before_health = get_column_health(
            st.session_state.dirty_df,
            selected_column
        )

        after_health = get_column_health(
            st.session_state.preview_df,
            selected_column
        )

        before_col, after_col = st.columns(2)

        with before_col:
            st.write("##### Before")
            for label, value in before_health.items():
                st.metric(label, value)

        with after_col:
            st.write("##### After")
            for label, value in after_health.items():
                st.metric(label, value)


# =========================
# S7v1 - Column Reports
# =========================
st.write("### Column Reports")

with st.container(border=True):

    # S7.1v1 - Report Layout Columns
    btn_col, report_col = st.columns([1, 3])

    with btn_col:

        # S7.2v1 - Report Buttons
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        if st.button("Return Rows with Missing Values", use_container_width=True):
            st.session_state.column_report = "rows_with_missing"

        if st.button("Return Transformation Mask", use_container_width=True):
            st.session_state.column_report = "missing_mask"

        if st.button("Return Duplicates", use_container_width=True):
            st.session_state.column_report = "duplicates"

        if st.button("Return Invalid Format Report", use_container_width=True):
            st.session_state.column_report = "invalid_format_report"

    with report_col:

        # S7.3v1 - Report Display Logic
        if "column_report" not in st.session_state:
            st.info("Select a report to view.")

        elif st.session_state.column_report == "rows_with_missing":
            st.write("### Rows with Missing Values")
            st.dataframe(
                return_rows_with_missing_values(st.session_state.dirty_df),
                use_container_width=True
            )

        elif st.session_state.column_report == "missing_mask":
            st.write("### Transformation Mask")
            st.dataframe(
                return_transformation_mask(st.session_state.dirty_mask),
                use_container_width=True
            )

        elif st.session_state.column_report == "duplicates":
            st.write("### Duplicate Rows")
            st.dataframe(
                return_duplicates(st.session_state.dirty_df),
                use_container_width=True
            )

        elif st.session_state.column_report == "invalid_format_report":
            st.write("### Invalid Format Report")
            st.dataframe(
                return_invalid_format_report(
                    st.session_state.dirty_df,
                    st.session_state.dirty_mask
                ),
                use_container_width=True
            )

# =========================
# S8v1 - Export Reports
# =========================
st.write("### Export Reports")

with st.container(border=True):

    export_col1, export_col2, export_col3 = st.columns(3)

    cleaned_csv = st.session_state.dirty_df.to_csv(index=False).encode("utf-8")

    mask_csv = st.session_state.dirty_mask.to_csv(index=False).encode("utf-8")

    invalid_report_df = return_invalid_format_report(
        st.session_state.dirty_df,
        st.session_state.dirty_mask
    )

    invalid_report_csv = invalid_report_df.to_csv(index=False).encode("utf-8")

    with export_col1:
        st.download_button(
            label="Download Cleaned Dataset",
            data=cleaned_csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col2:
        st.download_button(
            label="Download Transformation Mask",
            data=mask_csv,
            file_name="transformation_mask.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col3:
        st.download_button(
            label="Download Invalid Format Report",
            data=invalid_report_csv,
            file_name="invalid_format_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    transformation_code = generate_transformation_code(
        st.session_state.transformation_steps
    ).encode("utf-8")

    st.download_button(
        label="Download Transformation Code",
        data=transformation_code,
        file_name="transformation_code.py",
        mime="text/x-python",
        use_container_width=True
    )

st.write("")
