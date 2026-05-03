# CHIP 705 Open Payments General Payments Analysis

## Project overview

This project analyzes CMS Open Payments General Payments data using Python. Open Payments is a public transparency program that reports payments and other transfers of value from drug and medical device companies to covered recipients such as physicians and teaching hospitals.

## Research question

How do general industry payments to physicians vary by medical specialty, nature of payment, and state?

The analysis focuses on three smaller questions:

1. Which specialties receive the highest total and median general payment amounts?
2. Which nature-of-payment categories account for the largest number of payments and the largest total dollar amounts?
3. How do payment amounts in North Carolina compare with payment amounts in other states?

## Data source

Original data source: CMS Open Payments General Payments dataset  
https://openpaymentsdata.cms.gov/

The original Open Payments file was very large, so this repository uses a cleaned sample dataset extracted from the larger dataset. The cleaned file keeps only the fields needed for this project:

- `Covered_Recipient_Type`
- `Covered_Recipient_Specialty_1`
- `Recipient_State`
- `Nature_of_Payment_or_Transfer_of_Value`
- `Total_Amount_of_Payment_USDollars`
- `Date_of_Payment`

## Files in this repository

```text
README.md
open_payments_analysis.ipynb
requirements.txt
data/
  cleaned_general_payments_sample.csv
outputs/
  top_specialties_chart.png
  payment_category_chart.png
  nc_comparison_chart.png
  specialty_summary.csv
  nature_of_payment_summary.csv
  nc_vs_other_summary.csv
```

## How to run the analysis

1. Clone or download this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Open `open_payments_analysis.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.
4. Run the notebook from top to bottom.

## Python packages used

- pandas
- numpy
- matplotlib

## Summary of analysis steps

The notebook:

1. Loads the cleaned Open Payments dataset.
2. Filters to physician recipients.
3. Cleans payment amount and date fields.
4. Creates summary tables by specialty, nature of payment, and state.
5. Compares North Carolina with all other states.
6. Creates visualizations and saves output files.

## Limitations

This project uses a cleaned sample extracted from a larger CMS Open Payments dataset. The results are useful for demonstrating the Python analysis workflow, but they should not be interpreted as complete national totals unless the notebook is rerun using the full dataset.
