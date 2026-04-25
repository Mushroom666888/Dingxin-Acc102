from pathlib import Path
import pandas as pd


# =========================
# Layer 1: Data Cleaning and ESG Classification
# =========================

# 1. Set file paths
DATA_PATH = Path("data/esg_social_data.xlsx")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# 2. Load the Excel file
# The first row is a title row, so the real column names start from the second row.
raw_df = pd.read_excel(
    DATA_PATH,
    sheet_name="Data used in analysis",
    header=1
)

# 3. Remove fully empty columns
raw_df = raw_df.dropna(axis=1, how="all")

# 4. Clean column names
raw_df = raw_df.rename(columns={
    "ESG_ score": "ESG_score",
    "G _score": "G_score"
})

# 5. Keep only the seven core variables
core_columns = [
    "Year",
    "Company",
    "ESG_score",
    "E_score",
    "S_score",
    "G_score",
    "ROA"
]

core_df = raw_df[core_columns].copy()

# 6. Convert numeric columns to numeric format
numeric_columns = [
    "Year",
    "ESG_score",
    "E_score",
    "S_score",
    "G_score",
    "ROA"
]

for col in numeric_columns:
    core_df[col] = pd.to_numeric(core_df[col], errors="coerce")

# 7. Basic data checks
print("===== Basic Data Check =====")
print("Shape of core dataset:", core_df.shape)
print("Number of companies:", core_df["Company"].nunique())
print("Year range:", core_df["Year"].min(), "-", core_df["Year"].max())
print("Missing values:")
print(core_df.isna().sum())

# 8. Calculate company-level average E, S, G, ESG, and ROA
company_summary = (
    core_df
    .groupby("Company", as_index=False)
    .agg(
        Avg_E_score=("E_score", "mean"),
        Avg_S_score=("S_score", "mean"),
        Avg_G_score=("G_score", "mean"),
    )
)

# 9. Construct Weighted ESG alpha
company_summary["Alpha_Weighted_ESG"] = (
    0.4 * company_summary["Avg_E_score"]
    + 0.4 * company_summary["Avg_S_score"]
    + 0.2 * company_summary["Avg_G_score"]
)

# 10. Classify companies based on alpha
def classify_company(alpha):
    if alpha > 50:
        return "Top-tier Synergy Leaders"
    elif alpha >= 40:
        return "Middle-tier Standard Group"
    else:
        return "Bottom-tier Social Traps"


company_summary["ESG_Category"] = company_summary["Alpha_Weighted_ESG"].apply(classify_company)

# 11. Rank companies by alpha
company_summary = company_summary.sort_values(
    by="Alpha_Weighted_ESG",
    ascending=False
).reset_index(drop=True)

company_summary.insert(0, "Rank", company_summary.index + 1)

# 12. Merge the category back to the original seven-column panel data
classified_df = core_df.merge(
    company_summary[["Company", "Alpha_Weighted_ESG", "ESG_Category"]],
    on="Company",
    how="left"
)

# 13. Split the seven-column panel data into three tables
top_tier_table = classified_df.loc[
    classified_df["ESG_Category"] == "Top-tier Synergy Leaders",
    core_columns
].copy()

middle_tier_table = classified_df.loc[
    classified_df["ESG_Category"] == "Middle-tier Standard Group",
    core_columns
].copy()

bottom_tier_table = classified_df.loc[
    classified_df["ESG_Category"] == "Bottom-tier Social Traps",
    core_columns
].copy()

# 14. Sort each table by company and year
top_tier_table = top_tier_table.sort_values(["Company", "Year"]).reset_index(drop=True)
middle_tier_table = middle_tier_table.sort_values(["Company", "Year"]).reset_index(drop=True)
bottom_tier_table = bottom_tier_table.sort_values(["Company", "Year"]).reset_index(drop=True)

# 15. Print alpha ranking and group sizes
print("\n===== Company-level Alpha Ranking =====")
print(company_summary[[
    "Rank",
    "Company",
    "Avg_E_score",
    "Avg_S_score",
    "Avg_G_score",
    "Alpha_Weighted_ESG",
    "ESG_Category"
]].to_string(index=False))

print("\n===== Group Sizes =====")
print("Top-tier rows:", len(top_tier_table))
print("Middle-tier rows:", len(middle_tier_table))
print("Bottom-tier rows:", len(bottom_tier_table))

# 16. Save only the four required Layer 1 output tables
company_summary.to_csv(
    OUTPUT_DIR / "layer1_company_alpha_ranking.csv",
    index=False
)

top_tier_table.to_csv(
    OUTPUT_DIR / "layer1_top_tier_synergy_leaders.csv",
    index=False
)

middle_tier_table.to_csv(
    OUTPUT_DIR / "layer1_middle_tier_standard_group.csv",
    index=False
)

bottom_tier_table.to_csv(
    OUTPUT_DIR / "layer1_bottom_tier_social_traps.csv",
    index=False
)

print("\nLayer 1 completed successfully.")
print("Only four Layer 1 output tables have been saved:")
print("1. layer1_company_alpha_ranking.csv")
print("2. layer1_top_tier_synergy_leaders.csv")
print("3. layer1_middle_tier_standard_group.csv")
print("4. layer1_bottom_tier_social_traps.csv")