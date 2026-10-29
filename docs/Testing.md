# Testing Guide

## Manual testing checklist

1. Run the dashboard with:
   ```bash
   streamlit run app.py
   ```
2. Open the app and verify the sample dataset loads automatically.
3. Upload a CSV file with different columns and confirm the summary updates.
4. Check that charts render without errors.
5. Try natural-language questions such as:
   - top sales region
   - summary
   - missing values
   - highest product sales
6. Verify the downloaded report is created in the `reports` folder.

## Sample validation expectations

- Summary metrics should update correctly
- Missing values should be counted accurately
- Duplicate rows should be reported
- Charts should not break if some columns are absent
- The natural-language Q&A should provide fallback guidance when a question is unsupported
