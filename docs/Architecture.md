# AI Data Analyst Dashboard

## Overview

The AI Data Analyst dashboard is a lightweight analytics application that helps users upload a CSV or Excel dataset, inspect data quality, and generate summary insights. It combines structured analysis with a simple rule-based question-answer feature to simulate an AI analyst experience.

## Key modules

### `app.py`
The main Streamlit application entry point. It handles file uploads, displays dashboard cards, renders charts, and provides the natural-language Q&A input.

### `src/data_analyzer.py`
This module contains the logic for loading datasets, computing summary statistics, generating insights, and building visualizations.

## Workflow

1. User uploads a CSV or Excel file.
2. The system reads the file and shows a preview.
3. The app calculates missing values, duplicates, and dataset dimensions.
4. Summary cards highlight the most important measures.
5. Charts visualize sales, profits, and data quality.
6. A Q&A box answers common questions from the dataset.

## Data expectations

The application works best with tabular data containing columns like:

- Date
- Region
- Product
- Sales
- Profit
- Units Sold
- Customer Satisfaction

## Why this project matters

This dashboard demonstrates end-to-end thinking in data analytics: ingestion, cleaning, summarization, visualization, and insight extraction. It is a strong portfolio project for showcasing analytical and presentation skills.
