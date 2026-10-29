# README.md
# AI Data Analyst

A complete and practical AI-powered data analysis dashboard built with Python and Streamlit. This project helps users upload CSV or Excel files, review their data, visualize trends, and ask natural-language questions about the dataset.

## Project goals

- Analyze structured datasets quickly
- Detect missing values and duplicates
- Showcase key business insights
- Provide simple interactive charts
- Offer a lightweight AI-style Q&A layer
- Be easy to run and present for scholarship or portfolio submissions

## Features

- Upload CSV or Excel files
- Browse dataset preview
- Show row, column, missing value, and duplicate summaries
- Generate business-friendly insights automatically
- Display sales and profit charts
- Ask simple questions like:
  - "What is the top sales region?"
  - "What are the missing values?"
  - "Give me a summary of the dataset"
- Export a text report for sharing

## Tech stack

- Python 3.10+
- Streamlit
- Pandas
- Plotly
- NumPy

## Project structure

```text
AI-Data-Analyst/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_sales_data.csv
├── src/
│   ├── __init__.py
│   └── data_analyzer.py
├── docs/
│   ├── API_Documentation.md
│   ├── Architecture.md
│   ├── Roadmap.md
│   └── Testing.md
├── reports/
└── .gitignore
```

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Run the application

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Sample usage

- Upload `data/sample_sales_data.csv` or any CSV/Excel file
- Review the summary cards and charts
- Ask a question in the sidebar input box
- Download the generated report

## Example questions

- What is the top sales region?
- Which product has the highest sales?
- Are there missing values?
- Give me a summary of the dataset
- Show me the trend over time

## Submission-ready value

This project is designed to demonstrate practical data science and analytics skills in a portfolio or scholarship submission. It covers data cleaning, visualization, analytical reasoning, and a user-facing dashboard.

## License

This project is intended for educational and personal use.
