import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("data/cleaned_general_payments_sample.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

needed_columns = [
    "Covered_Recipient_Type",
    "Covered_Recipient_Specialty_1",
    "Recipient_State",
    "Nature_of_Payment_or_Transfer_of_Value",
    "Total_Amount_of_Payment_USDollars",
    "Date_of_Payment"
]

df = df[needed_columns].copy()
df = df[df["Covered_Recipient_Type"] == "Covered Recipient Physician"].copy()
df["Total_Amount_of_Payment_USDollars"] = pd.to_numeric(df["Total_Amount_of_Payment_USDollars"], errors="coerce")
df["Date_of_Payment"] = pd.to_datetime(df["Date_of_Payment"], errors="coerce")
df = df.dropna(subset=[
    "Covered_Recipient_Specialty_1",
    "Recipient_State",
    "Nature_of_Payment_or_Transfer_of_Value",
    "Total_Amount_of_Payment_USDollars",
    "Date_of_Payment"
])

specialty_summary = (
    df.groupby("Covered_Recipient_Specialty_1")
    .agg(
        total_payment=("Total_Amount_of_Payment_USDollars", "sum"),
        median_payment=("Total_Amount_of_Payment_USDollars", "median"),
        number_of_payments=("Total_Amount_of_Payment_USDollars", "count")
    )
    .reset_index()
    .sort_values("total_payment", ascending=False)
)

nature_summary = (
    df.groupby("Nature_of_Payment_or_Transfer_of_Value")
    .agg(
        total_payment=("Total_Amount_of_Payment_USDollars", "sum"),
        median_payment=("Total_Amount_of_Payment_USDollars", "median"),
        number_of_payments=("Total_Amount_of_Payment_USDollars", "count")
    )
    .reset_index()
    .sort_values("total_payment", ascending=False)
)

df["NC_vs_Other"] = np.where(df["Recipient_State"] == "NC", "North Carolina", "Other states")
nc_summary = (
    df.groupby("NC_vs_Other")
    .agg(
        total_payment=("Total_Amount_of_Payment_USDollars", "sum"),
        median_payment=("Total_Amount_of_Payment_USDollars", "median"),
        number_of_payments=("Total_Amount_of_Payment_USDollars", "count")
    )
    .reset_index()
)

specialty_summary.to_csv(OUTPUT_DIR / "specialty_summary.csv", index=False)
nature_summary.to_csv(OUTPUT_DIR / "nature_of_payment_summary.csv", index=False)
nc_summary.to_csv(OUTPUT_DIR / "nc_vs_other_summary.csv", index=False)

top_specialties = specialty_summary.head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_specialties["Covered_Recipient_Specialty_1"], top_specialties["total_payment"])
plt.gca().invert_yaxis()
plt.title("Top 10 Specialties by Total General Payment Amount")
plt.xlabel("Total Payment Amount (USD)")
plt.ylabel("Specialty")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_specialties_chart.png", dpi=150, bbox_inches="tight")
plt.close()

top_nature = nature_summary.head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_nature["Nature_of_Payment_or_Transfer_of_Value"], top_nature["total_payment"])
plt.gca().invert_yaxis()
plt.title("Top Nature-of-Payment Categories by Total Amount")
plt.xlabel("Total Payment Amount (USD)")
plt.ylabel("Nature of Payment")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "payment_category_chart.png", dpi=150, bbox_inches="tight")
plt.close()

plt.figure(figsize=(7, 5))
plt.bar(nc_summary["NC_vs_Other"], nc_summary["median_payment"])
plt.title("Median General Payment: North Carolina vs Other States")
plt.xlabel("Recipient location")
plt.ylabel("Median Payment Amount (USD)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "nc_comparison_chart.png", dpi=150, bbox_inches="tight")
plt.close()

print("Analysis complete.")
print("Rows analyzed:", len(df))
print("Output files saved in:", OUTPUT_DIR)
