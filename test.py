import random
import pandas as pd
import streamlit as st
import base64
from pathlib import Path


# =========================
# Dirty Data Generator
# =========================

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


# =========================
# App Functions Being Tested
# =========================

def strip_whitespace(dataframe):
    return dataframe.map(
        lambda value: value.strip() if isinstance(value, str) else value
    )


def convert_to_lowercase(dataframe):
    return dataframe.map(
        lambda value: value.lower() if isinstance(value, str) else value
    )


def return_duplicates(dataframe):
    return dataframe[dataframe.duplicated()]


def drop_duplicates(dataframe):
    return dataframe.drop_duplicates()


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


def convert_col_to_datetime(dataframe, column_name):
    dataframe = dataframe.copy()
    dataframe[column_name] = pd.to_datetime(
        dataframe[column_name],
        errors="coerce"
    )
    return dataframe


def convert_iso_date_pattern(dataframe, column_name):
    df = dataframe.copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = df[column_name].astype(str).str.strip()
    mask = cleaned.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)

    converted = pd.to_datetime(
        cleaned[mask],
        format="%Y-%m-%d",
        errors="coerce"
    )

    valid_mask = mask.copy()
    valid_mask.loc[mask] = converted.notna()

    df.loc[valid_mask, column_name] = converted[converted.notna()]
    return df


def convert_us_dash_date_pattern(dataframe, column_name):
    df = dataframe.copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = df[column_name].astype(str).str.strip()
    mask = cleaned.str.match(r"^\d{2}-\d{2}-\d{4}$", na=False)

    converted = pd.to_datetime(
        cleaned[mask],
        format="%m-%d-%Y",
        errors="coerce"
    )

    valid_mask = mask.copy()
    valid_mask.loc[mask] = converted.notna()

    df.loc[valid_mask, column_name] = converted[converted.notna()]
    return df


def convert_us_slash_date_pattern(dataframe, column_name):
    df = dataframe.copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = df[column_name].astype(str).str.strip()
    mask = cleaned.str.match(r"^\d{2}/\d{2}/\d{4}$", na=False)

    converted = pd.to_datetime(
        cleaned[mask],
        format="%m/%d/%Y",
        errors="coerce"
    )

    valid_mask = mask.copy()
    valid_mask.loc[mask] = converted.notna()

    df.loc[valid_mask, column_name] = converted[converted.notna()]
    return df


def convert_text_month_date_pattern(dataframe, column_name):
    df = dataframe.copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = df[column_name].astype(str).str.strip().str.lower()
    mask = cleaned.str.match(r"^[a-zA-Z]+\s+\d{1,2}\s+\d{4}$", na=False)

    converted = pd.to_datetime(
        cleaned[mask],
        format="%B %d %Y",
        errors="coerce"
    )

    valid_mask = mask.copy()
    valid_mask.loc[mask] = converted.notna()

    df.loc[valid_mask, column_name] = converted[converted.notna()]
    return df


def convert_iso_slash_date_pattern(dataframe, column_name):
    df = dataframe.copy()
    df[column_name] = df[column_name].astype("object")

    cleaned = df[column_name].astype(str).str.strip()
    mask = cleaned.str.match(r"^\d{4}/\d{2}/\d{2}$", na=False)

    converted = pd.to_datetime(
        cleaned[mask],
        format="%Y/%m/%d",
        errors="coerce"
    )

    valid_mask = mask.copy()
    valid_mask.loc[mask] = converted.notna()

    df.loc[valid_mask, column_name] = converted[converted.notna()]
    return df


def convert_common_date_patterns(dataframe, column_name):
    df = dataframe.copy()

    df = convert_iso_date_pattern(df, column_name)
    df = convert_us_dash_date_pattern(df, column_name)
    df = convert_us_slash_date_pattern(df, column_name)
    df = convert_text_month_date_pattern(df, column_name)
    df = convert_iso_slash_date_pattern(df, column_name)

    return df


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


def get_row_count(dataframe):
    return len(dataframe)


def get_column_count(dataframe):
    return len(dataframe.columns)


def count_duplicate_rows(dataframe):
    return dataframe.duplicated().sum()


def count_total_missing_values(dataframe):
    return dataframe.isna().sum().sum()


def count_rows_with_missing_values(dataframe):
    return dataframe.isna().any(axis=1).sum()


def get_missing_values_by_column(dataframe):
    return dataframe.isna().sum()


def get_missing_percent_by_column(dataframe):
    if len(dataframe) == 0:
        return pd.Series(0, index=dataframe.columns)

    return (dataframe.isna().sum() / len(dataframe)) * 100


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
        "rows_with_missing": count_rows_with_missing_values(dataframe),
        "missing_by_column": get_missing_percent_by_column(dataframe),
        "missing_row_percent": get_missing_row_percent(dataframe),
    }


def get_column_health(dataframe, column_name):
    column = dataframe[column_name]
    total_rows = len(column)

    if total_rows == 0:
        return {
            "Missing %": "0%",
            "Unique": 0,
            "Duplicates": 0,
            "Numeric Valid %": "0%",
            "Datetime Valid %": "0%",
        }

    missing_percent = column.isna().sum() / total_rows * 100
    unique_count = column.nunique(dropna=True)
    duplicate_count = column.duplicated().sum()

    numeric_converted = pd.to_numeric(column, errors="coerce")
    numeric_valid_percent = (
        numeric_converted.notna().sum() / column.notna().sum() * 100
        if column.notna().sum() > 0 else 0
    )

    datetime_converted = pd.to_datetime(column, errors="coerce")
    datetime_valid_percent = (
        datetime_converted.notna().sum() / column.notna().sum() * 100
        if column.notna().sum() > 0 else 0
    )

    return {
        "Missing %": f"{missing_percent:.0f}%",
        "Unique": unique_count,
        "Duplicates": duplicate_count,
        "Numeric Valid %": f"{numeric_valid_percent:.0f}%",
        "Datetime Valid %": f"{datetime_valid_percent:.0f}%",
    }


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


# =========================
# Streamlit Dirty Data Display
# =========================
st.set_page_config(
    page_title="Function Test Page",
    page_icon="🧪",
    layout="wide"
)

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


st.title("Function Test Page")


# =========================
# Dirty Data Display
# =========================

st.write("### Data Frame Transformation Section")


with st.container(border=True):
    left_panel, right_panel = st.columns([1, 6])

    with left_panel:
        record_count = st.number_input(
            "Enter number of records",
            min_value=1,
            max_value=1000,
            value=25,
            step=1
        )

        if "dirty_df" not in st.session_state:
            st.session_state.dirty_df = generate_dirty_data(record_count)

        if st.button("Generate Data", use_container_width=True):
            st.session_state.dirty_df = generate_dirty_data(record_count)
            st.session_state.preview_df = st.session_state.dirty_df.copy()

        st.write("")

        if st.button("Strip Whitespace", use_container_width=True):
            st.session_state.dirty_df = strip_whitespace(
                st.session_state.dirty_df
            )

        if st.button("Convert to Lowercase", use_container_width=True):
            st.session_state.dirty_df = convert_to_lowercase(
                st.session_state.dirty_df
            )

        if st.button("Drop Duplicates", use_container_width=True):
            st.session_state.dirty_df = drop_duplicates(
                st.session_state.dirty_df
            )

        if st.button("Fill Missing Values", use_container_width=True):
            st.session_state.dirty_df = fill_missing_values(
                st.session_state.dirty_df
            )

    with right_panel:
        st.dataframe(st.session_state.dirty_df, use_container_width=True)


# =========================
# Data Health Dashboard
# =========================

summary = get_data_health_summary(st.session_state.dirty_df)
missing_by_column = summary["missing_by_column"]


with st.container(border=True):
    left_panel, right_panel = st.columns([1, 2])


with left_panel:
    with st.container(border=True):
        st.write("#### Row Health")

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric("Rows", summary["row_count"])

        with metric_col2:
            st.metric("Duplicates", summary["duplicate_count"])

        with metric_col3:
            st.metric("Rows w/ Missing", summary["rows_with_missing"])

        with metric_col4:
            st.metric("Incomplete Rows %",
                      f"{summary['missing_row_percent']:.0f}%")

with right_panel:
    with st.container(border=True):
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
# Column Transformation Preview
# =========================

st.write("### Column Transformations")

with st.container(border=True):

    left, right = st.columns([2, 3])

    with left:
        selected_column = st.selectbox(
            "Select a column to transform",
            st.session_state.dirty_df.columns
        )

    if "preview_df" not in st.session_state:
        st.session_state.preview_df = st.session_state.dirty_df.copy()

    if "last_selected_column" not in st.session_state:
        st.session_state.last_selected_column = selected_column

    if st.session_state.last_selected_column != selected_column:
        st.session_state.preview_df = st.session_state.dirty_df.copy()
        st.session_state.last_selected_column = selected_column

    transform_col, blank_col1, compare_col, blank_col2, health_col = st.columns([
        2, 1, 4, 1, 4
    ])

    with transform_col:
        st.write("#### Transformations")
        st.write("")
        st.write("")

        if st.button("Convert to Numeric", key="col_convert_numeric", use_container_width=True):
            st.session_state.preview_df = convert_col_to_numeric(
                st.session_state.preview_df,
                selected_column
            )

        if st.button("Convert to Datetime", key="col_convert_datetime", use_container_width=True):
            st.session_state.preview_df = convert_common_date_patterns(
                st.session_state.preview_df,
                selected_column
            )

        if st.button("Fill Missing", key="col_fill_missing", use_container_width=True):
            st.session_state.preview_df = fill_missing_values_in_column(
                st.session_state.preview_df,
                selected_column
            )

        if st.button("Convert ISO Date Pattern", key="col_flag_missing", use_container_width=True):
            st.session_state.preview_df = convert_iso_date_pattern(
                st.session_state.preview_df,
                selected_column
            )

        st.write("")

        if st.button("Apply Changes to DataFrame", key="apply_column_preview", use_container_width=True):
            st.session_state.dirty_df = st.session_state.preview_df.copy()
            st.session_state.preview_df = st.session_state.dirty_df.copy()
            st.rerun()

    with compare_col:
        st.write(f"#### Original vs Preview: {selected_column}")

        compare_df = pd.DataFrame({
            f"Original: {selected_column}": st.session_state.dirty_df[selected_column],
            f"Preview: {selected_column}": st.session_state.preview_df[selected_column]
        })

        st.dataframe(compare_df, use_container_width=True, height=450)

    with health_col:
        st.write("#### Column Health Preview")

        before_health = get_column_health(
            st.session_state.dirty_df,
            selected_column
        )

        after_health = get_column_health(
            st.session_state.preview_df,
            selected_column
        )

        conversion_success = get_conversion_success_percent(
            st.session_state.dirty_df,
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

            st.metric("Converted Successfully %", conversion_success)


# =========================
# Column Reports
# =========================

st.write("### Column Reports")

with st.container(border=True):

    btn_col, report_col = st.columns([1, 3])

    with btn_col:
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        if st.button("Return Rows with Missing Values", use_container_width=True):
            st.session_state.column_report = "rows_with_missing"

        if st.button("Return Missing Mask", use_container_width=True):
            st.session_state.column_report = "missing_mask"

        if st.button("Return Duplicates", use_container_width=True):
            st.session_state.column_report = "duplicates"

        if st.button("Return Failed Clean Type Rows", use_container_width=True):
            st.session_state.column_report = "failed_clean_type_rows"

    with report_col:
        if "column_report" not in st.session_state:
            st.info("Select a report to view.")

        elif st.session_state.column_report == "rows_with_missing":
            st.write("### Rows with Missing Values")
            st.dataframe(
                return_rows_with_missing_values(st.session_state.dirty_df),
                use_container_width=True
            )

        elif st.session_state.column_report == "missing_mask":
            st.write("### Missing Value Mask")
            st.dataframe(
                return_missing_mask(st.session_state.dirty_df),
                use_container_width=True
            )

        elif st.session_state.column_report == "duplicates":
            st.write("### Duplicate Rows")
            st.dataframe(
                return_duplicates(st.session_state.dirty_df),
                use_container_width=True
            )
        elif st.session_state.column_report == "failed_clean_type_rows":
            st.write(
                f"### Rows Where `{selected_column}` Could Not Convert Cleanly")
            st.dataframe(
                return_failed_clean_type_rows(
                    st.session_state.dirty_df,
                    selected_column
                ),
                use_container_width=True
            )

st.write("")
