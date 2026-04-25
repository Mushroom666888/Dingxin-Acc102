from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# =========================
# Layer 2 - Script 2
# One dual-axis trend plot based on yearly group averages
# =========================

# 1. Set paths
OUTPUT_DIR = Path("outputs")
LAYER2_DIR = OUTPUT_DIR / "layer2"
FIGURE_DIR = LAYER2_DIR / "script2_dual_axis_group_average_trend"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# 2. Define input files from Layer 1
top_file = OUTPUT_DIR / "layer1_top_tier_synergy_leaders.csv"
middle_file = OUTPUT_DIR / "layer1_middle_tier_standard_group.csv"
bottom_file = OUTPUT_DIR / "layer1_bottom_tier_social_traps.csv"

# 3. Define output figure file
output_figure = FIGURE_DIR / "layer2_script2_dual_axis_group_average_trend.png"

# 4. Read data
top_df = pd.read_csv(top_file)
middle_df = pd.read_csv(middle_file)
bottom_df = pd.read_csv(bottom_file)

# 5. Add category labels
top_df["ESG_Category"] = "Top-tier Synergy Leaders"
middle_df["ESG_Category"] = "Middle-tier Standard Group"
bottom_df["ESG_Category"] = "Bottom-tier Social Traps"

# 6. Combine the three group tables
combined_df = pd.concat([top_df, middle_df, bottom_df], ignore_index=True)

# 7. Keep required columns only
combined_df = combined_df[["Year", "ESG_Category", "ESG_score", "ROA"]].copy()

# 8. Convert key columns to numeric
combined_df["Year"] = pd.to_numeric(combined_df["Year"], errors="coerce")
combined_df["ESG_score"] = pd.to_numeric(combined_df["ESG_score"], errors="coerce")
combined_df["ROA"] = pd.to_numeric(combined_df["ROA"], errors="coerce")

# 9. Drop invalid rows
combined_df = combined_df.dropna(subset=["Year", "ESG_Category", "ESG_score", "ROA"]).copy()

# 10. Calculate yearly averages for each category
group_average_df = (
    combined_df
    .groupby(["Year", "ESG_Category"], as_index=False)
    .agg(
        Avg_ESG_score=("ESG_score", "mean"),
        Avg_ROA=("ROA", "mean")
    )
)

# 11. Sort data
group_average_df = group_average_df.sort_values(["ESG_Category", "Year"]).reset_index(drop=True)

# 12. Map Year to index 1, 2, 3, ..., 8
years = sorted(group_average_df["Year"].unique())
year_to_index = {year: idx + 1 for idx, year in enumerate(years)}
group_average_df["Year_Index"] = group_average_df["Year"].map(year_to_index)

# 13. Define category order and colours
category_order = [
    "Top-tier Synergy Leaders",
    "Middle-tier Standard Group",
    "Bottom-tier Social Traps"
]

category_colours = {
    "Top-tier Synergy Leaders": "tab:blue",
    "Middle-tier Standard Group": "tab:orange",
    "Bottom-tier Social Traps": "tab:green"
}

# 14. Create figure and twin axes
fig, ax_esg = plt.subplots(figsize=(14, 8))
ax_roa = ax_esg.twinx()

# 15. Plot lines for each category
for category in category_order:
    temp_df = group_average_df[group_average_df["ESG_Category"] == category].copy()
    colour = category_colours[category]

    # ESG_score: dashed line on left axis
    ax_esg.plot(
        temp_df["Year_Index"],
        temp_df["Avg_ESG_score"],
        linestyle="--",
        marker="o",
        linewidth=2.6,
        markersize=6.5,
        color=colour,
        alpha=0.95
    )

    # ROA: solid line on right axis
    ax_roa.plot(
        temp_df["Year_Index"],
        temp_df["Avg_ROA"],
        linestyle="-",
        marker="s",
        linewidth=2.6,
        markersize=6.0,
        color=colour,
        alpha=0.95
    )

# 16. Axis settings
ax_esg.set_title(
    "Average ESG Score and ROA Trends by ESG Category",
    fontsize=17,
    fontweight="bold",
    pad=14
)

ax_esg.set_xlabel(
    "Year Index (1 = 2015, 2 = 2016, ..., 8 = 2022)",
    fontsize=13
)
ax_esg.set_ylabel("Average ESG Score", fontsize=13)
ax_roa.set_ylabel("Average ROA", fontsize=13)

ax_esg.set_xticks(list(range(1, len(years) + 1)))
ax_esg.set_xticklabels([str(i) for i in range(1, len(years) + 1)], fontsize=11)

ax_esg.tick_params(axis="y", labelsize=11)
ax_roa.tick_params(axis="y", labelsize=11)

# 17. Add margins to make the plot clearer
ax_esg.set_xlim(0.7, len(years) + 0.3)

esg_min = group_average_df["Avg_ESG_score"].min()
esg_max = group_average_df["Avg_ESG_score"].max()
esg_range = esg_max - esg_min
ax_esg.set_ylim(esg_min - 0.12 * esg_range, esg_max + 0.12 * esg_range)

roa_min = group_average_df["Avg_ROA"].min()
roa_max = group_average_df["Avg_ROA"].max()
roa_range = roa_max - roa_min
ax_roa.set_ylim(roa_min - 0.15 * roa_range, roa_max + 0.15 * roa_range)

# 18. Grid
ax_esg.grid(True, linestyle="--", alpha=0.30)

# 19. Legends
# Legend 1: variable styles
style_handles = [
    Line2D(
        [0], [0],
        color="black",
        linestyle="--",
        marker="o",
        linewidth=2.5,
        label="Average ESG Score (left axis, dashed)"
    ),
    Line2D(
        [0], [0],
        color="black",
        linestyle="-",
        marker="s",
        linewidth=2.5,
        label="Average ROA (right axis, solid)"
    )
]

legend1 = ax_esg.legend(
    handles=style_handles,
    loc="upper left",
    fontsize=10,
    frameon=True
)
ax_esg.add_artist(legend1)

# Legend 2: category colours
category_handles = [
    Line2D(
        [0], [0],
        color=category_colours[category],
        linewidth=2.8,
        label=category
    )
    for category in category_order
]

ax_esg.legend(
    handles=category_handles,
    title="ESG Category",
    loc="upper left",
    bbox_to_anchor=(1.02, 0.88),
    fontsize=10,
    title_fontsize=11,
    frameon=True
)
# 20. Save figure
fig.tight_layout()
fig.savefig(output_figure, dpi=300, bbox_inches="tight")
plt.close(fig)

# 21. Print summary
print("Layer 2 - Script 2 completed successfully.")
print(f"Saved figure: {output_figure}")
print("\nPreview of yearly group averages:")
print(group_average_df.to_string(index=False))