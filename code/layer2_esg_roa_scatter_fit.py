from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# Layer 2 - Script 1
# ESG_score vs ROA Scatter Plots with Linear Fit
# =========================

# 1. Set paths
OUTPUT_DIR = Path("outputs")
LAYER2_DIR = OUTPUT_DIR / "layer2"
FIGURE_DIR = LAYER2_DIR / "script1_esg_roa_scatter_fit"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# 2. Define input files from Layer 1
group_files = {
    "Top-tier Synergy Leaders": OUTPUT_DIR / "layer1_top_tier_synergy_leaders.csv",
    "Middle-tier Standard Group": OUTPUT_DIR / "layer1_middle_tier_standard_group.csv",
    "Bottom-tier Social Traps": OUTPUT_DIR / "layer1_bottom_tier_social_traps.csv",
}

# 3. Define output figure names
figure_files = {
    "Top-tier Synergy Leaders": FIGURE_DIR / "layer2_script1_top_tier_esg_roa.png",
    "Middle-tier Standard Group": FIGURE_DIR / "layer2_script1_middle_tier_esg_roa.png",
    "Bottom-tier Social Traps": FIGURE_DIR / "layer2_script1_bottom_tier_esg_roa.png",
}


def calculate_linear_fit(x, y):
    """
    Calculate a simple linear regression line:
    ROA = intercept + slope * ESG_score
    """
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept

    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    if ss_tot == 0:
        r_squared = np.nan
    else:
        r_squared = 1 - ss_res / ss_tot

    return slope, intercept, r_squared


def plot_esg_roa_relationship(group_name, file_path, output_path):
    """
    Plot ESG_score vs ROA for one ESG classification group.

    Each company-year observation is plotted as one point.
    Different companies are shown with different colours.
    A group-level linear regression line is added as a reference trend.
    """
    # 1. Read the classified table
    df = pd.read_csv(file_path)

    # 2. Keep valid observations only
    df = df.dropna(subset=["Company", "ESG_score", "ROA"]).copy()

    # 3. Convert key variables to numeric format
    df["ESG_score"] = pd.to_numeric(df["ESG_score"], errors="coerce")
    df["ROA"] = pd.to_numeric(df["ROA"], errors="coerce")
    df = df.dropna(subset=["ESG_score", "ROA"])

    # 4. Extract x and y values
    x = df["ESG_score"].to_numpy()
    y = df["ROA"].to_numpy()

    # 5. Calculate group-level linear fit
    slope, intercept, r_squared = calculate_linear_fit(x, y)

    # 6. Create a wider x range for the regression line
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    x_range = x_max - x_min
    y_range = y_max - y_min

    # Add margins so the plot looks more stretched and less crowded
    x_margin = 0.12 * x_range if x_range != 0 else 1
    y_margin = 0.15 * y_range if y_range != 0 else 1

    x_plot_min = x_min - x_margin
    x_plot_max = x_max + x_margin
    y_plot_min = y_min - y_margin
    y_plot_max = y_max + y_margin

    x_line = np.linspace(x_plot_min, x_plot_max, 300)
    y_line = slope * x_line + intercept

    # 7. Create figure: make it longer and wider
    plt.figure(figsize=(13, 7.5))

    companies = sorted(df["Company"].unique())

    # 8. Plot points company by company
    for company in companies:
        company_df = df[df["Company"] == company]

        plt.scatter(
            company_df["ESG_score"],
            company_df["ROA"],
            s=60,
            alpha=0.85,
            label=company
        )

    # 9. Plot the linear regression reference line
    plt.plot(
        x_line,
        y_line,
        linewidth=2.8,
        linestyle="--",
        label=f"Linear fit: ROA = {slope:.3f} × ESG_score + {intercept:.3f}, R² = {r_squared:.3f}"
    )

    # 10. Figure formatting
    plt.title(
        f"Relationship between ESG Score and ROA\n{group_name}",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("ESG Score", fontsize=13)
    plt.ylabel("ROA", fontsize=13)

    # Make axes longer / more spacious
    plt.xlim(x_plot_min, x_plot_max)
    plt.ylim(y_plot_min, y_plot_max)

    plt.grid(True, linestyle="--", alpha=0.35)

    # Put legend outside the plot area
    plt.legend(
        fontsize=8,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=True
    )

    plt.tight_layout()

    # 11. Save figure
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    # 12. Print summary
    print(f"Saved figure: {output_path}")
    print(f"{group_name}")
    print(f"  Number of observations: {len(df)}")
    print(f"  Number of companies: {df['Company'].nunique()}")
    print(f"  Slope: {slope:.4f}")
    print(f"  Intercept: {intercept:.4f}")
    print(f"  R-squared: {r_squared:.4f}")
    print("-" * 60)


# 4. Run plotting for all three ESG groups
for group_name, file_path in group_files.items():
    plot_esg_roa_relationship(
        group_name=group_name,
        file_path=file_path,
        output_path=figure_files[group_name]
    )

print("\nLayer 2 - Script 1 completed successfully.")
print("Three ESG_score vs ROA scatter-fit figures have been saved in:")
print("outputs/layer2/script1_esg_roa_scatter_fit")