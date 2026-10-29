# app.py
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.data_analyzer import (
    answer_user_question,
    build_chart,
    export_summary_report,
    generate_insights,
    load_dataset,
    preview_dataframe,
    summarize_dataframe,
)


st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")
st.title("📊 AI Data Analyst Dashboard")
st.caption("Upload a CSV or Excel file to explore data, uncover insights, and ask simple questions.")

sample_data_path = Path(__file__).resolve().parent / "data" / "sample_sales_data.csv"

with st.sidebar:
    st.header("Dataset")
    uploaded_file = st.file_uploader("Upload CSV or Excel spreadsheet", type=["csv", "xlsx", "xls"])
    st.markdown("---")
    st.markdown("### Quick tips")
    st.markdown("- Upload a file with numeric and dates columns for richer visual analysis.")
    st.markdown("- Use the AI Q&A box to ask dataset questions like 'top sales region' or 'missing values'.")

if uploaded_file is not None:
    df = load_dataset(uploaded_file)
    st.session_state["dataset_loaded"] = True
else:
    if sample_data_path.exists():
        df = pd.read_csv(sample_data_path)
    else:
        st.warning("No dataset available. Please upload a file.")
        st.stop()

summary = summarize_dataframe(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", f"{summary['rows']:,}")
col2.metric("Columns", summary["columns"])
col3.metric("Missing Values", f"{summary['missing_cells']:,}")
col4.metric("Duplicate Rows", f"{summary['duplicate_rows']:,}")

st.subheader("Dataset Preview")
preview = preview_dataframe(df, rows=10)
st.dataframe(preview, use_container_width=True)

st.subheader("Data Quality Summary")
missing_df = pd.DataFrame(
    {
        "Column": list(summary["missing_by_column"].keys()),
        "Missing Values": list(summary["missing_by_column"].values()),
    }
)
missing_df = missing_df[missing_df["Missing Values"] > 0]
if missing_df.empty:
    st.info("No missing values detected.")
else:
    st.bar_chart(missing_df.set_index("Column"))

st.subheader("Key Insights")
insights = generate_insights(df)
for insight in insights:
    st.markdown(f"- {insight}")

st.subheader("Visual Analysis")
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    if {"Region", "Sales"}.issubset(df.columns):
        st.plotly_chart(build_chart(df, "sales_by_region"), use_container_width=True)
with chart_col2:
    if {"Product", "Profit"}.issubset(df.columns):
        st.plotly_chart(build_chart(df, "profit_by_product"), use_container_width=True)

chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    if {"Date", "Sales"}.issubset(df.columns):
        st.plotly_chart(build_chart(df, "sales_over_time"), use_container_width=True)
with chart_col4:
    if {"Sales", "Profit"}.issubset(df.columns):
        st.plotly_chart(build_chart(df, "sales_vs_profit"), use_container_width=True)

st.subheader("Ask the Analyst")
question = st.text_input("Type a question about the dataset", "What is the top sales region?")
if st.button("Get Answer"):
    st.info(answer_user_question(df, question))

st.subheader("Export Report")
report = export_summary_report(df)
st.text_area("Generated report", report, height=250)

if st.button("Download report"):
    report_path = Path("reports") / "ai_data_analyst_report.txt"
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    st.success(f"Report saved to {report_path}")

st.markdown("---")
st.caption("Built for AI Data Analyst project submissions.")
