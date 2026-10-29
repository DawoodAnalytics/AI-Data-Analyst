from pathlib import Path

import pandas as pd
import plotly.express as px


DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_sales_data.csv"


def load_dataset(file=None):
    """Load CSV or Excel file. Falls back to sample data if no file is supplied."""
    if file is not None:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        if file.name.endswith((".xlsx", ".xls")):
            return pd.read_excel(file)
        raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")

    if DATASET_PATH.exists():
        return pd.read_csv(DATASET_PATH)

    raise FileNotFoundError("Sample dataset not found.")


def summarize_dataframe(df):
    """Return summary metrics for the dataframe."""
    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_cells": int(df.isna().sum().sum()),
        "missing_by_column": df.isna().sum().sort_values(ascending=False).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": list(df.select_dtypes(include=["number"]).columns),
        "categorical_columns": list(df.select_dtypes(exclude=["number"]).columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }
    return summary


def top_performing_region(df):
    if "Region" in df.columns and "Sales" in df.columns:
        return (
            df.groupby("Region")["Sales"].sum().sort_values(ascending=False).head(1).to_dict()
        )
    return {}


def top_product(df):
    if "Product" in df.columns and "Sales" in df.columns:
        return (
            df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(1).to_dict()
        )
    return {}


def generate_insights(df):
    """Generate a list of human-readable insights from the dataset."""
    insights = []
    summary = summarize_dataframe(df)

    if summary["rows"]:
        insights.append(f"The dataset contains {summary['rows']} rows and {summary['columns']} columns.")

    missing_columns = [
        (col, value) for col, value in summary["missing_by_column"].items() if value > 0
    ]
    if missing_columns:
        col, count = missing_columns[0]
        insights.append(f"The column '{col}' has the highest number of missing values ({count}).")

    if summary["duplicate_rows"]:
        insights.append(f"There are {summary['duplicate_rows']} duplicated rows in the dataset.")
    else:
        insights.append("There are no duplicate rows in the dataset.")

    top_region = top_performing_region(df)
    if top_region:
        region, sales = next(iter(top_region.items()))
        insights.append(f"The strongest region is {region} with total sales of {sales:,.2f}.")

    top_product_name = top_product(df)
    if top_product_name:
        product, sales = next(iter(top_product_name.items()))
        insights.append(f"The best-selling product is {product}, generating {sales:,.2f} in sales.")

    numeric_cols = summary["numeric_columns"]
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True)
        if not corr.empty:
            max_corr = corr.where(~pd.DataFrame(np.eye(len(corr)), index=corr.index, columns=corr.columns).astype(bool)).stack().idxmax()
            insights.append(
                f"The strongest numerical relationship is between {max_corr[0]} and {max_corr[1]} "
                f"with a correlation score of {corr.loc[max_corr]:.2f}."
            )

    return insights


def answer_user_question(df, question):
    """A lightweight rule-based assistant for common questions about the dataset."""
    q = question.lower()
    summary = summarize_dataframe(df)

    if "summary" in q or "overview" in q:
        return (
            f"This dataset has {summary['rows']} rows, {summary['columns']} columns, "
            f"{summary['missing_cells']} missing values, and {summary['duplicate_rows']} duplicate rows."
        )

    if "missing" in q:
        missing = summary["missing_by_column"]
        if missing:
            col, count = max(missing.items(), key=lambda item: item[1])
            return f"The most incomplete column is '{col}' with {count} missing values."
        return "There are no missing values in the dataset."

    if "top" in q and "sales" in q:
        region = top_performing_region(df)
        if region:
            name, value = next(iter(region.items()))
            return f"The top sales region is {name} with total sales of {value:,.2f}."

    if "top" in q and "product" in q:
        product = top_product(df)
        if product:
            name, value = next(iter(product.items()))
            return f"The top product by sales is {name} with {value:,.2f} in sales."

    if "trend" in q or "time" in q:
        if "Date" in df.columns and "Sales" in df.columns:
            timeline = df.groupby("Date")["Sales"].sum().reset_index()
            start = timeline["Sales"].iloc[0]
            end = timeline["Sales"].iloc[-1]
            direction = "increasing" if end > start else "decreasing"
            return (
                f"Sales trend is {direction} over time, starting at {start:,.2f} and ending at {end:,.2f}."
            )

    if "region" in q and "best" in q:
        region = top_performing_region(df)
        if region:
            name, value = next(iter(region.items()))
            return f"Best-performing region: {name} with {value:,.2f} total sales."

    return "I can answer questions about totals, missing values, best regions, top products, and trends."


def export_summary_report(df):
    """Create a plain-text report summary of the dataset."""
    summary = summarize_dataframe(df)
    lines = [
        "AI Data Analyst Report",
        "====================",
        f"Rows: {summary['rows']}",
        f"Columns: {summary['columns']}",
        f"Missing Values: {summary['missing_cells']}",
        f"Duplicate Rows: {summary['duplicate_rows']}",
        "",
        "Top insights:",
    ]
    lines.extend(f"- {insight}" for insight in generate_insights(df))
    return "\n".join(lines)


def build_chart(df, chart_type="sales_by_region"):
    if chart_type == "sales_by_region":
        if "Region" in df.columns and "Sales" in df.columns:
            chart_data = df.groupby("Region", as_index=False)["Sales"].sum()
            return px.bar(chart_data, x="Region", y="Sales", title="Total Sales by Region")

    if chart_type == "sales_over_time":
        if "Date" in df.columns and "Sales" in df.columns:
            chart_data = df.groupby("Date", as_index=False)["Sales"].sum()
            chart_data["Date"] = pd.to_datetime(chart_data["Date"])
            return px.line(chart_data, x="Date", y="Sales", title="Sales Over Time")

    if chart_type == "profit_by_product":
        if "Product" in df.columns and "Profit" in df.columns:
            chart_data = df.groupby("Product", as_index=False)["Profit"].sum()
            return px.bar(chart_data, x="Product", y="Profit", color="Product", title="Profit by Product")

    if chart_type == "missing_values":
        missing = df.isna().sum().reset_index()
        missing.columns = ["Column", "MissingValues"]
        missing = missing[missing["MissingValues"] > 0]
        if missing.empty:
            return px.bar(title="No missing values detected")
        return px.bar(missing, x="Column", y="MissingValues", title="Missing Values by Column")

    if chart_type == "sales_vs_profit":
        if {"Sales", "Profit"}.issubset(df.columns):
            return px.scatter(df, x="Sales", y="Profit", title="Sales vs Profit")

    return px.bar(title="Chart not available for this dataset")


def preview_dataframe(df, rows=10):
    return df.head(rows)


# This import is needed for the correlation logic in generate_insights
import numpy as np
"""
This module serves as the analysis engine for the AI Data Analyst Dashboard.
It contains dataset loading, summaries, insights generation, and visualization helpers.
"""

__all__ = [
    "load_dataset",
    "summarize_dataframe",
    "generate_insights",
    "answer_user_question",
    "export_summary_report",
    "build_chart",
    "preview_dataframe",
]
"""