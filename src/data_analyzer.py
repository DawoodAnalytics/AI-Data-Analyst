from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px


def _normalize_columns(df: pd.DataFrame) -> dict[str, str]:
    return {str(column).strip().lower(): str(column) for column in df.columns}


def _pick_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    column_map = _normalize_columns(df)
    for candidate in candidates:
        if candidate in column_map:
            return column_map[candidate]
    return None


def load_dataset(uploaded_file: Any) -> pd.DataFrame:
    """Load a CSV or Excel file uploaded through Streamlit."""
    if uploaded_file is None:
        raise ValueError("No dataset uploaded.")

    filename = str(getattr(uploaded_file, "name", "")).lower()
    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if filename.endswith((".xls", ".xlsx")):
        return pd.read_excel(uploaded_file)
    raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")


def summarize_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    """Return a summary dictionary for a dataframe."""
    missing_by_column = df.isnull().sum().to_dict()
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_cells": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_by_column": {str(k): int(v) for k, v in missing_by_column.items()},
    }


def preview_dataframe(df: pd.DataFrame, rows: int = 10) -> pd.DataFrame:
    return df.head(rows).copy()


def generate_insights(df: pd.DataFrame) -> list[str]:
    """Create a few simple insights from the dataframe."""
    insights: list[str] = []

    if df.empty:
        return ["The uploaded dataset is empty."]

    summary = summarize_dataframe(df)
    total_rows = summary["rows"]
    missing_total = summary["missing_cells"]
    insights.append(f"The dataset contains {total_rows:,} rows and {summary['columns']} columns.")

    if missing_total > 0:
        insights.append(f"There are {missing_total:,} missing values across the dataset.")
    else:
        insights.append("No missing values were found in the dataset.")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        col = numeric_cols[0]
        insights.append(f"The '{col}' column is numeric and has a total of {df[col].sum():,.2f}.")

    if "sales" in _normalize_columns(df):
        sales_col = _pick_column(df, ["sales", "revenue", "amount", "total_sales"])
        if sales_col:
            total_sales = df[sales_col].sum()
            insights.append(f"Total sales amount is {total_sales:,.2f}.")

    return insights[:5]


def answer_user_question(df: pd.DataFrame, question: str) -> str:
    """Answer basic questions about the dataframe using simple heuristics."""
    q = (question or "").strip().lower()
    if not q:
        return "Please ask a question about the dataset."

    summary = summarize_dataframe(df)
    column_map = _normalize_columns(df)

    if any(word in q for word in ["missing", "null", "blank", "na"]):
        missing_total = summary["missing_cells"]
        return f"There are {missing_total:,} missing values in the dataset."

    if any(word in q for word in ["summary", "overview", "describe", "tell me about"]):
        return (
            f"This dataset has {summary['rows']:,} rows, {summary['columns']} columns, "
            f"{summary['missing_cells']:,} missing values, and {summary['duplicate_rows']:,} duplicate rows."
        )

    sales_col = _pick_column(df, ["sales", "revenue", "amount", "total_sales"])
    region_col = _pick_column(df, ["region", "country", "market", "segment", "category"])
    if ("top" in q or "highest" in q or "best" in q) and sales_col and region_col:
        top_region = (
            df.groupby(region_col, dropna=False)[sales_col].sum().sort_values(ascending=False).head(1)
        )
        if not top_region.empty:
            region_name = str(top_region.index[0])
            region_value = float(top_region.iloc[0])
            return f"The top sales region is {region_name} with {region_value:,.2f}."

    if "duplicate" in q:
        return f"There are {summary['duplicate_rows']:,} duplicate rows in the dataset."

    if "columns" in q or "fields" in q:
        return "Columns: " + ", ".join(str(col) for col in df.columns)

    if "rows" in q:
        return f"The dataset has {summary['rows']:,} rows."

    if q.startswith("what is") and sales_col:
        return f"The total sales in the dataset is {df[sales_col].sum():,.2f}."

    if any(word in q for word in ["top", "max", "largest"]) and sales_col:
        top_value = df[sales_col].max()
        return f"The maximum value in '{sales_col}' is {top_value:,.2f}."

    return "I can answer simple dataset questions like totals, missing values, duplicates, and top sales regions."


def build_chart(df: pd.DataFrame, chart_type: str) -> Any:
    """Return a Plotly chart object based on the requested chart type."""
    column_map = _normalize_columns(df)

    if chart_type == "sales_by_region":
        region_col = _pick_column(df, ["region", "country", "market", "segment"])
        sales_col = _pick_column(df, ["sales", "revenue", "amount", "total_sales"])
        if region_col and sales_col:
            grouped = df.groupby(region_col, dropna=False)[sales_col].sum().reset_index()
            return px.bar(grouped, x=region_col, y=sales_col, title="Sales by Region")

    if chart_type == "profit_by_product":
        product_col = _pick_column(df, ["product", "item", "product_name"])
        profit_col = _pick_column(df, ["profit", "gross_profit", "net_profit"])
        if product_col and profit_col:
            grouped = df.groupby(product_col, dropna=False)[profit_col].sum().reset_index()
            return px.bar(grouped, x=product_col, y=profit_col, title="Profit by Product")

    if chart_type == "sales_over_time":
        date_col = _pick_column(df, ["date", "order_date", "transaction_date", "timestamp"])
        sales_col = _pick_column(df, ["sales", "revenue", "amount", "total_sales"])
        if date_col and sales_col:
            working = df[[date_col, sales_col]].copy()
            working[date_col] = pd.to_datetime(working[date_col], errors="coerce")
            working = working.dropna(subset=[date_col])
            weekly = working.groupby(working[date_col].dt.to_period("M").astype(str))[sales_col].sum().reset_index()
            weekly = weekly.rename(columns={"index": date_col}) if False else weekly
            return px.line(weekly, x=weekly.columns[0], y=weekly.columns[1], title="Sales Over Time")

    if chart_type == "sales_vs_profit":
        sales_col = _pick_column(df, ["sales", "revenue", "amount", "total_sales"])
        profit_col = _pick_column(df, ["profit", "gross_profit", "net_profit"])
        if sales_col and profit_col:
            return px.scatter(df, x=sales_col, y=profit_col, title="Sales vs Profit")

    if len(df.columns) >= 2:
        x_col = df.columns[0]
        y_col = df.columns[1]
        return px.scatter(df, x=x_col, y=y_col, title="Dataset Scatter Plot")

    return px.bar(df.head(10), x=df.columns[0], y=df.index, title="Dataset Preview")


def export_summary_report(df: pd.DataFrame) -> str:
    """Export a readable summary as plain text."""
    summary = summarize_dataframe(df)
    lines = [
        "AI Data Analyst Summary Report",
        "=" * 30,
        f"Rows: {summary['rows']:,}",
        f"Columns: {summary['columns']}",
        f"Missing values: {summary['missing_cells']:,}",
        f"Duplicate rows: {summary['duplicate_rows']:,}",
        "",
        "Missing by column:",
    ]

    if summary["missing_by_column"]:
        for column, count in summary["missing_by_column"].items():
            lines.append(f"- {column}: {count}")
    else:
        lines.append("- None")

    lines.extend(["", "Insights:"])
    for insight in generate_insights(df):
        lines.append(f"- {insight}")

    return "\n".join(lines)
