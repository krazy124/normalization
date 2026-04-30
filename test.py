import random
import pandas as pd
import streamlit as st


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


# =========================
# Streamlit Dirty Data Display
# =========================
st.set_page_config(
    page_title="Function Test Page",
    page_icon="🧪",
    layout="wide"
)

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

        if st.button("Generate New Dirty Data", use_container_width=True):
            st.session_state.dirty_df = generate_dirty_data(record_count)

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

st.write("### Data Health Dashboard")

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
# Transformation Buttons
# =========================

col1, col2 = st.columns(2)

with col1:

    if st.button("Return Rows with Missing Values"):
        st.write("### Rows with Missing Values")
        st.dataframe(
            return_rows_with_missing_values(st.session_state.dirty_df),
            use_container_width=True
        )

    if st.button("Return Missing Mask"):
        st.write("### Missing Value Mask")
        st.dataframe(
            return_missing_mask(st.session_state.dirty_df),
            use_container_width=True
        )
    if st.button("Return Duplicates"):
        st.write("### Duplicate Rows")
        st.dataframe(
            return_duplicates(st.session_state.dirty_df),
            use_container_width=True
        )

with col2:
    if st.button("Count Duplicate Rows"):
        st.write("### Duplicate Row Count")
        st.write(count_duplicate_rows(st.session_state.dirty_df))

    if st.button("Count Missing Values"):
        st.write("### Missing Values Count")
        st.dataframe(
            count_missing_values(
                st.session_state.dirty_df
            ).to_frame("missing_count"),
            use_container_width=True
        )


# =========================
# Column Transformation Preview
# =========================

st.write("---")
st.write("### Column Transformations")

selected_column = st.selectbox(
    "Select a column to transform",
    st.session_state.dirty_df.columns
)

preview_df = st.session_state.dirty_df.copy()

transform_col, original_col, preview_col = st.columns([1, 2, 2])

with transform_col:
    st.write("#### Transformations")

    if st.button("Convert to Numeric", key="col_convert_numeric"):
        preview_df = convert_col_to_numeric(preview_df, selected_column)

    if st.button("Show Failed Numeric Rows", key="col_failed_numeric"):
        preview_df = return_failed_numeric_conversions(
            preview_df,
            selected_column
        )

    if st.button("Convert to Datetime", key="col_convert_datetime"):
        preview_df = convert_col_to_datetime(preview_df, selected_column)

    if st.button("Show Failed Datetime Rows", key="col_failed_datetime"):
        preview_df = return_failed_datetime_conversions(
            preview_df,
            selected_column
        )

    if st.button("Fill Missing", key="col_fill_missing"):
        preview_df = fill_missing_values_in_column(
            preview_df,
            selected_column
        )

    if st.button("Show Missing Rows", key="col_show_missing"):
        preview_df = return_rows_with_missing_values_in_column(
            preview_df,
            selected_column
        )

with original_col:
    st.write(f"#### Original: {selected_column}")
    st.dataframe(
        st.session_state.dirty_df[[selected_column]],
        use_container_width=True
    )

with preview_col:
    st.write(f"#### Preview: {selected_column}")

    if selected_column in preview_df.columns:
        st.dataframe(
            preview_df[[selected_column]],
            use_container_width=True
        )
    else:
        st.dataframe(
            preview_df,
            use_container_width=True
        )

    if st.button("Apply Changes to DataFrame", key="apply_column_preview"):
        st.session_state.dirty_df = preview_df.copy()
        st.rerun()
