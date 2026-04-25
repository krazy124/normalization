# normalization
Interactive data profiling and normalization tool that scans messy datasets, highlights anomalies, recommends transformations, and helps users clean data with confidence.

Data Normalization Assistant

Interactive data profiling and normalization tool that scans messy datasets, highlights anomalies, recommends transformations, and helps users clean data with confidence.

Overview

Data Normalization Assistant is a Python-based data cleaning and profiling tool built to help users quickly assess dataset quality and apply common normalization steps through an interactive interface.

The app is designed to:

profile uploaded datasets
identify anomalies and data quality issues
recommend common cleaning actions
apply transformations interactively
compare changes before and after transformation
export cleaned data for downstream use

This project was built as both:

a practical tool for daily data work
a portfolio project demonstrating data engineering workflow design, data quality validation, and transformation logic
Features
Upload CSV datasets
Preview raw data
Scan columns for data quality issues
Detect missing values, duplicates, and invalid types
Highlight anomalies and suspicious values
Recommend transformation options by column
Compare before and after transformations
Export cleaned datasets
Track applied transformations
Core Data Cleaning Functions
Trim whitespace
Standardize text casing
Parse and normalize dates
Handle missing values
Detect and remove duplicates
Validate data types
Detect outliers
Standardize categorical values
Normalize numeric ranges
Encode categorical columns
Tech Stack
Python
Pandas
Streamlit
Plotly / Matplotlib
ydata-profiling

Planned:

AWS deployment
transformation pipeline export
reusable cleaning profiles
How It Works
Upload a dataset
Profile the data
Review detected issues
Apply recommended transformations
Compare before and after results
Export cleaned data
Project Goals

This project focuses on building a practical, explainable data-cleaning workflow that helps users understand not only what should be changed in a dataset, but why.

The goal is to make data normalization:

interactive
explainable
reusable
easier to trust
Future Improvements
Export transformations as reusable Python pipeline code
Add user-defined transformation rules
Add batch processing support
Add advanced anomaly scoring
Deploy public web version
