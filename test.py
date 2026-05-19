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


import pandas as pd
import streamlit as st
import base64
from io import StringIO
from pathlib import Path

from transformations import *


# F37v1
def add_transformation_step(function_name, column_name):
    if "transformation_steps" not in st.session_state:
        st.session_state.transformation_steps = []

    st.session_state.transformation_steps.append({
        "function": function_name,
        "column": column_name
    })

# F38v1


@st.dialog("Upload CSV")
def open_csv_upload_dialog():
    uploaded_csv = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        key="csv_file_uploader"
    )

    pasted_csv = st.text_area(
        "Or paste CSV text here",
        height=200,
        key="csv_text_input"
    )

    import_col, cancel_col = st.columns(2)

    with import_col:
        if st.button("Import CSV", use_container_width=True):
            if uploaded_csv is not None:
                uploaded_df = pd.read_csv(uploaded_csv)
            elif pasted_csv.strip() != "":
                uploaded_df = pd.read_csv(StringIO(pasted_csv))
            else:
                st.warning("Upload a CSV file or paste CSV text first.")
                return

            st.session_state.dirty_df = uploaded_df
            st.session_state.dirty_mask = create_or_update_transformation_mask(
                uploaded_df)
            st.session_state.preview_df = uploaded_df.copy()
            st.session_state.preview_mask = st.session_state.dirty_mask.copy()
            st.session_state.transformation_steps = []
            st.rerun()

    with cancel_col:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


# =========================S1v1 - Streamlit Page Setup=========================
st.set_page_config(
    page_title="Function Test Page",
    page_icon="🧪",
    layout="wide"
)


# =========================S2v1 - App Styling=========================
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


# =========================S3v1 - Main Title=========================
st.title("Function Test Page")


# =========================S4v2 - Dirty Data Display Section=========================
st.write("### Data Frame Transformation Section")

with st.container(border=True):

    # S4.1v1 - Layout Columns
    left_panel, right_panel = st.columns([1, 6])

    with left_panel:

        # S4.2v2 - CSV Import Button

        if st.button("Upload CSV", use_container_width=True):
            open_csv_upload_dialog()

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
            st.session_state.dirty_df = Transformation.strip_whitespace(
                st.session_state.dirty_df
            )

        if st.button("Convert to Lowercase", use_container_width=True):
            st.session_state.dirty_df = Transformation.convert_to_lowercase(
                st.session_state.dirty_df
            )

        if st.button("Drop Duplicates", use_container_width=True):
            st.session_state.dirty_df, st.session_state.dirty_mask = drop_duplicates(
                st.session_state.dirty_df,
                st.session_state.dirty_mask
            )

    with right_panel:

        # S4.6v1 - Dirty DataFrame Display
        st.dataframe(st.session_state.dirty_df, use_container_width=True)


# =========================S5v1 - Data Health Dashboard=========================
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


# =========================S6v2 - Column Transformation Preview=========================
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

        # S6.5v5 - Column Transformation Buttons
        st.write("#### Transformations")
        st.write("")
        st.write("")

        if st.button("Convert to Float", key="col_convert_numeric", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=Transformation.to_float_keep_failed,
                mask_df=st.session_state.preview_mask
            )
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
                transformation_function=Transformation.fill_missing_unknown,
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
                transformation_function=Transformation.to_titlecase,
                mask_df=st.session_state.preview_mask
            )
            add_transformation_step("convert_to_titlecase", selected_column)

        if st.button("Convert to Lowercase", key="col_convert_lowercase", use_container_width=True):
            st.session_state.preview_df, st.session_state.preview_mask = run_column_transformation(
                dataframe=st.session_state.preview_df,
                column_name=selected_column,
                transformation_function=Transformation.to_lowercase,
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
        st.write("")

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
            # S6.6v4 - Original vs Preview Compare Table
            compare_df = sort_transformation_preview(
                compare_df,
                original_column,
                preview_column,
                st.session_state.preview_mask[selected_column]
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


# =========================S7v1 - Column Reports=========================
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

# =========================S8v1 - Export Reports=========================
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
