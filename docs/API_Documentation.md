# API Documentation

This project does not currently expose a network API. Instead, it acts as a local data analysis dashboard run using Streamlit.

## Core functions

### `load_dataset(file=None)`
Loads either a uploaded CSV/Excel file or the bundled sample dataset.

### `summarize_dataframe(df)`
Returns a dictionary with the number of rows, columns, missing cells, duplicate rows, and variable types.

### `generate_insights(df)`
Creates a human-readable list of key data insights.

### `answer_user_question(df, question)`
Answers common questions such as:
- top sales region
- top product by sales
- missing values
- summary overview
- sales trend over time

### `build_chart(df, chart_type)`
Creates visualizations using Plotly for bar charts, scatter plots, and trend charts.

### `export_summary_report(df)`
Generates a plain-text report that can be saved to disk.
