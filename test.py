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


def get_missing_values_by_column(dataframe):
    return dataframe.isna().sum()


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
        "missing_by_column": get_missing_values_by_column(dataframe),
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
st.subheader("Dirty Data Generator Test")

record_count = st.number_input(
    "Enter number of records",
    min_value=1,
    max_value=1000,
    value=25,
    step=1
)

dirty_df = generate_dirty_data(record_count)

st.write("### Dirty Data")
st.dataframe(dirty_df, use_container_width=True)


if st.button("Convert Dirty Data to Lowercase"):
    dirty_df = convert_to_lowercase(dirty_df)

    st.write("### Lowercase Data")
    st.dataframe(dirty_df, use_container_width=True)

# =========================
# Function Test Buttons
# =========================

if st.button("Strip Whitespace"):
    result_df = strip_whitespace(dirty_df)
    st.write("### Strip Whitespace Result")
    st.dataframe(result_df, use_container_width=True)

if st.button("Convert to Lowercase"):
    result_df = convert_to_lowercase(dirty_df)
    st.write("### Convert to Lowercase Result")
    st.dataframe(result_df, use_container_width=True)

if st.button("Return Duplicates"):
    result_df = return_duplicates(dirty_df)
    st.write("### Duplicate Rows")
    st.dataframe(result_df, use_container_width=True)

if st.button("Drop Duplicates"):
    result_df = drop_duplicates(dirty_df)
    st.write("### Drop Duplicates Result")
    st.dataframe(result_df, use_container_width=True)

if st.button("Count Missing Values"):
    result_series = count_missing_values(dirty_df)
    st.write("### Missing Values Count")
    st.dataframe(result_series.to_frame(
        "missing_count"), use_container_width=True)

if st.button("Return Missing Mask"):
    result_df = return_missing_mask(dirty_df)
    st.write("### Missing Value Mask")
    st.dataframe(result_df, use_container_width=True)

if st.button("Return Rows with Missing Values"):
    result_df = return_rows_with_missing_values(dirty_df)
    st.write("### Rows with Missing Values")
    st.dataframe(result_df, use_container_width=True)

if st.button("Fill Missing Values"):
    result_df = fill_missing_values(dirty_df)
    st.write("### Fill Missing Values Result")
    st.dataframe(result_df, use_container_width=True)

if st.button("Get Row Count"):
    st.write("### Row Count")
    st.write(get_row_count(dirty_df))

if st.button("Get Column Count"):
    st.write("### Column Count")
    st.write(get_column_count(dirty_df))

if st.button("Count Duplicate Rows"):
    st.write("### Duplicate Row Count")
    st.write(count_duplicate_rows(dirty_df))

if st.button("Count Total Missing Values"):
    st.write("### Total Missing Values")
    st.write(count_total_missing_values(dirty_df))

if st.button("Get Missing Values by Column"):
    result_series = get_missing_values_by_column(dirty_df)
    st.write("### Missing Values by Column")
    st.dataframe(result_series.to_frame(
        "missing_count"), use_container_width=True)

if st.button("Get Missing Row Percent"):
    st.write("### Missing Row Percent")
    st.write(get_missing_row_percent(dirty_df))

if st.button("Get Data Health Summary"):
    summary = get_data_health_summary(dirty_df)

    st.write("### Data Health Summary")
    st.write(f"Row Count: {summary['row_count']}")
    st.write(f"Column Count: {summary['column_count']}")
    st.write(f"Duplicate Count: {summary['duplicate_count']}")
    st.write(f"Total Missing: {summary['total_missing']}")
    st.write(f"Missing Row Percent: {summary['missing_row_percent']:.2f}%")
    st.dataframe(
        summary["missing_by_column"].to_frame("missing_count"),
        use_container_width=True
    )
