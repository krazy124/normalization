"""Streamlit app for the Data Normalization Assistant.

Collapse this section when not in use to keep the file easier to scan.
Use as a quick reference for available app utilities.

DATAFRAME TRANSFORMATIONS
+-------------------------------------------+-----------------------------------------------+
| Function Name                             | Parameters                                    |
+-------------------------------------------+-----------------------------------------------+
| load_data                                 | file                                          |
| strip_whitespace                          | dataframe                                     |
| convert_to_lowercase                      | dataframe                                     |
| drop_duplicates                           | dataframe                                     |
| fill_missing_values                       | dataframe, fill_value="Unknown"               |
+-------------------------------------------+-----------------------------------------------+

DATAFRAME DIAGNOSTICS
+-------------------------------------------+-----------------------------------------------+
| Function Name                             | Parameters                                    |
+-------------------------------------------+-----------------------------------------------+
| return_duplicates                         | dataframe                                     |
| count_missing_values                      | dataframe                                     |
| return_missing_mask                       | dataframe                                     |
| return_rows_with_missing_values           | dataframe                                     |
| get_row_count                             | dataframe                                     |
| get_column_count                          | dataframe                                     |
| count_duplicate_rows                      | dataframe                                     |
| count_total_missing_values                | dataframe                                     |
| get_missing_values_by_column              | dataframe                                     |
| get_missing_percent_by_column             | dataframe                                     |
| get_missing_row_percent                   | dataframe                                     |
| get_data_health_summary                   | dataframe                                     |
+-------------------------------------------+-----------------------------------------------+

COLUMN TRANSFORMATIONS
+-------------------------------------------+-----------------------------------------------+
| Function Name                             | Parameters                                    |
+-------------------------------------------+-----------------------------------------------+
| convert_col_to_numeric                    | dataframe, column_name                        |
| convert_keep_failed_numeric_conversions   | dataframe, column_name                        |
| convert_to_int_with_na                    | dataframe, column_name                        |
| convert_col_to_datetime                   | dataframe, column_name                        |
| convert_keep_failed_datetime_conversions  | dataframe, column_name                        |
| fill_missing_values_in_column             | dataframe, column_name, fill_value="Unknown"  |
| preview_fill_missing_values_in_column     | dataframe, column_name, fill_value="Unknown"  |
| flag_missing_values_in_column             | dataframe, column_name                        |
+-------------------------------------------+-----------------------------------------------+

COLUMN DIAGNOSTICS
+-------------------------------------------+-----------------------------------------------+
| Function Name                             | Parameters                                    |
+-------------------------------------------+-----------------------------------------------+
| return_failed_numeric_conversions         | dataframe, column_name                        |
| return_failed_datetime_conversions        | dataframe, column_name                        |
| count_missing_values_in_column            | dataframe, column_name                        |
| return_rows_with_missing_values_in_column | dataframe, column_name                        |
+-------------------------------------------+-----------------------------------------------+
"""

import random
import pandas as pd
import re


class Transformation:
    @staticmethod
    def to_int_keep_failed(series):
        original = series.copy()
        cleaned = original.astype("string").str.strip()
        converted = pd.to_numeric(cleaned, errors="coerce")
        success_mask = converted.notna() & (converted % 1 == 0)

        result = original.astype("object").copy()
        result.loc[success_mask] = converted.loc[success_mask].astype("Int64")

        return result, success_mask

    @staticmethod
    def common_date_patterns(series):
        original = series.copy()
        cleaned = original.astype(str).str.strip()

        result = original.astype("object").copy()
        success_mask = pd.Series(False, index=series.index)

        date_patterns = [
            (r"^\d{4}-\d{2}-\d{2}$", "%Y-%m-%d"),
            (r"^\d{2}-\d{2}-\d{4}$", "%m-%d-%Y"),
            (r"^\d{2}/\d{2}/\d{4}$", "%m/%d/%Y"),
            (r"^[a-zA-Z]+\s+\d{1,2}\s+\d{4}$", "%B %d %Y"),
            (r"^\d{4}/\d{2}/\d{2}$", "%Y/%m/%d")
        ]

        for pattern, date_format in date_patterns:
            pattern_mask = cleaned.str.match(pattern, na=False) & ~success_mask

            converted = pd.to_datetime(
                cleaned[pattern_mask],
                format=date_format,
                errors="coerce"
            )

            converted_mask = converted.notna()
            converted_indexes = converted[converted_mask].index

            result.loc[converted_indexes] = converted.loc[converted_indexes]
            success_mask.loc[converted_indexes] = True

        return result, success_mask

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

        success_mask = cleaned.str.match(email_pattern, na=False)

        result = cleaned.where(success_mask | cleaned.isna(), original)

        return result, success_mask

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
        success_mask = converted.notna()

        result = original.astype("object").copy()
        result.loc[success_mask] = converted.loc[success_mask]

        return result, success_mask

    @staticmethod
    def to_titlecase(series):
        result = series.map(
            lambda value: value.title() if isinstance(value, str) else value
        )

        success_mask = pd.Series(True, index=series.index)

        return result, success_mask

    @staticmethod
    def to_lowercase(series):
        result = series.map(lambda value: value.lower()
                            if isinstance(value, str) else value)
        success_mask = pd.Series(True, index=series.index)
        return result, success_mask

    @staticmethod
    def fill_missing_unknown(series):
        result = series.fillna("Unknown")
        success_mask = pd.Series(True, index=series.index)
        return result, success_mask

    @staticmethod
    def strip_whitespace(dataframe):
        df = dataframe.copy()
        for column_name in df.columns:
            if (df[column_name].dtype == "object" or pd.api.types.is_string_dtype(df[column_name])):
                df[column_name] = df[column_name].map(lambda value: value.strip()
                                                      if isinstance(value, str)
                                                      else value)
        return df

    @staticmethod
    def convert_to_lowercase(dataframe):
        df = dataframe.copy()
        for column_name in df.columns:
            if (df[column_name].dtype == "object" or pd.api.types.is_string_dtype(df[column_name])):
                df[column_name] = df[column_name].map(
                    lambda value: value.lower() if isinstance(value, str) else value)
        return df

    @staticmethod
    def to_float_keep_failed(series):
        original = series.copy()
        converted = pd.to_numeric(original, errors="coerce")
        success_mask = converted.notna()

        result = original.astype("object").copy()
        result.loc[success_mask] = converted.loc[success_mask]

        return result, success_mask


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


# =========================Diagnostics=========================
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


# F12v1
def drop_duplicates(dataframe, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    df = df.drop_duplicates()
    mask_df = mask_df.reindex(index=df.index)

    return df, mask_df


# F13v1
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


# F14v1
def run_column_transformation(dataframe, column_name, transformation_function, mask_df=None):
    df = dataframe.copy()
    mask_df = create_or_update_transformation_mask(df, mask_df)

    original = df[column_name].copy()
    transformed, success_mask = transformation_function(original)

    df[column_name] = transformed

    missing_mask = original.isna() | original.astype(str).str.strip().eq("")
    changed_mask = original.astype(str) != transformed.astype(str)

    invalid_mask = ~missing_mask & ~success_mask
    cleaned_mask = ~missing_mask & success_mask & changed_mask
    valid_mask = ~missing_mask & success_mask & ~changed_mask

    mask_df.loc[missing_mask, column_name] = "missing"
    mask_df.loc[valid_mask, column_name] = "valid"
    mask_df.loc[cleaned_mask, column_name] = "cleaned"
    mask_df.loc[invalid_mask, column_name] = "invalid format"

    return df, mask_df


# F15v2
def sort_transformation_preview(compare_df, original_column, preview_column, mask_series=None):
    sorted_df = compare_df.copy()

    if mask_series is not None:
        sorted_df["_mask_status"] = mask_series.values

        sort_order = {
            "invalid format": 0,
            "cleaned": 1,
            "valid": 2,
            "missing": 3,
            "unprocessed": 4
        }

        sorted_df["_sort_group"] = sorted_df["_mask_status"].map(
            sort_order).fillna(5)

        sorted_df = sorted_df.sort_values(
            by="_sort_group",
            ascending=True
        )

        return sorted_df.drop(columns=["_sort_group", "_mask_status"])

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

# =========================Column Reports Sections=========================
# F16v1


def return_transformation_mask(mask_df):
    return mask_df.copy()


# F17v1
def return_rows_with_missing_values(dataframe):
    return dataframe[dataframe.isna().any(axis=1)]


# F18v1
def return_duplicates(dataframe):
    return dataframe[dataframe.duplicated()]


# F19v1
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


# =========================Invalid Format Section=========================
# F20v1
def get_invalid_format_reason(column_name, value):
    column_lower = column_name.lower()

    if "email" in column_lower:
        return get_email_invalid_reason(value)

    if "date" in column_lower:
        return get_datetime_invalid_reason(value)

    if "amount" in column_lower or "price" in column_lower:
        return get_currency_invalid_reason(value)

    return "Invalid format"


# F21v1
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


# F22v1
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


# F23v1
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


# =========================Transformation Code Generation=========================
# F24v1
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


# F25v2
def get_pure_transformation_code(function_name, column_name):
    templates = {
        "convert_col_to_numeric": f'''
    # Convert to Float: {column_name}
    converted = pd.to_numeric(df["{column_name}"], errors="coerce")
    df["{column_name}"] = converted.where(converted.notna(), df["{column_name}"])
''',

        "convert_to_int_keep_failed": f'''
    # Convert to Int: {column_name}
    converted = pd.to_numeric(df["{column_name}"].astype("string").str.strip(), errors="coerce")
    integer_converted = converted.where(converted % 1 == 0)
    df["{column_name}"] = integer_converted.astype("Int64").where(integer_converted.notna(), df["{column_name}"])
''',

        "convert_common_date_patterns": f'''
    # Convert to Datetime: {column_name}
    converted = pd.to_datetime(df["{column_name}"].astype("string").str.strip(), errors="coerce")
    df["{column_name}"] = converted.where(converted.notna(), df["{column_name}"])
''',

        "clean_and_validate_email_column": f'''
    # Clean / Validate Email: {column_name}
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,}}$"

    cleaned = (
        df["{column_name}"]
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\\s+", "", regex=True)
    )

    junk_values = ["", "na", "n/a", "none", "null", "nan"]
    cleaned = cleaned.mask(cleaned.isin(junk_values), pd.NA)

    valid_email = cleaned.str.match(email_pattern, na=False)
    df["{column_name}"] = cleaned.where(valid_email | cleaned.isna(), df["{column_name}"])
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
    df["{column_name}"] = converted.where(converted.notna(), df["{column_name}"])
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
