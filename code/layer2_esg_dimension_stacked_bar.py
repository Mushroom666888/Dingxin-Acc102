from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================
# Layer 2 - Script 3
# Grouped stacked bar chart for E, S, and G scores
# =========================

# 1. Set paths
OUTPUT_DIR = Path("outputs")
LAYER2_DIR = OUTPUT_DIR / "layer2"
FIGURE_DIR = LAYER2_DIR / "script3_esg_dimension_stacked_bar"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# 2. Define input files from Layer 1
top_file = OUTPUT_DIR / "layer1_top_tier_synergy_leaders.csv"
middle_file = OUTPUT_DIR / "layer1_middle_tier_standard_group.csv"
bottom_file = OUTPUT_DIR / "layer1_bottom_tier_social_traps.csv"

# 3. Define output figure file
output_figure = FIGURE_DIR / "layer2_script3_esg_dimension_stacked_bar.png"

# 4. Read the three classified tables
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
required_columns = [
    "Year",
    "ESG_Category",
    "E_score",
    "S_score",
    "G_score"
]

combined_df = combined_df[required_columns].copy()

# 8. Convert numeric columns
numeric_columns = ["Year", "E_score", "S_score", "G_score"]

for col in numeric_columns:
    combined_df[col] = pd.to_numeric(combined_df[col], errors="coerce")

# 9. Drop invalid rows
combined_df = combined_df.dropna(
    subset=["Year", "ESG_Category", "E_score", "S_score", "G_score"]
).copy()

# 10. Calculate yearly average E, S, and G scores for each category
group_average_df = (
    combined_df
    .groupby(["Year", "ESG_Category"], as_index=False)
    .agg(
        Avg_E_score=("E_score", "mean"),
        Avg_S_score=("S_score", "mean"),
        Avg_G_score=("G_score", "mean")
    )
)

# 11. Sort data
category_order = [
    "Top-tier Synergy Leaders",
    "Middle-tier Standard Group",
    "Bottom-tier Social Traps"
]

category_short_labels = {
    "Top-tier Synergy Leaders": "Top",
    "Middle-tier Standard Group": "Middle",
    "Bottom-tier Social Traps": "Bottom"
}

group_average_df["Category_Order"] = group_average_df["ESG_Category"].map({
    "Top-tier Synergy Leaders": 1,
    "Middle-tier Standard Group": 2,
    "Bottom-tier Social Traps": 3
})

group_average_df = group_average_df.sort_values(
    ["Year", "Category_Order"]
).reset_index(drop=True)

# 12. Map real years to year index: 1, 2, ..., 8
years = sorted(group_average_df["Year"].unique())
year_to_index = {year: idx + 1 for idx, year in enumerate(years)}
group_average_df["Year_Index"] = group_average_df["Year"].map(year_to_index)

# 13. Prepare bar positions
x_positions = np.arange(1, len(years) + 1)
bar_width = 0.23

category_offsets = {
    "Top-tier Synergy Leaders": -bar_width,
    "Middle-tier Standard Group": 0,
    "Bottom-tier Social Traps": bar_width
}

# 14. Define colours for E, S, and G score layers
dimension_colours = {
    "E_score": "#4C78A8",
    "S_score": "#F58518",
    "G_score": "#54A24B"
}

# 15. Create figure
fig, ax = plt.subplots(figsize=(15, 8.5))

# 16. Plot grouped stacked bars
for category in category_order:
    temp_df = group_average_df[group_average_df["ESG_Category"] == category].copy()
    temp_df = temp_df.sort_values("Year_Index")

    x = temp_df["Year_Index"].to_numpy() + category_offsets[category]

    e_values = temp_df["Avg_E_score"].to_numpy()
    s_values = temp_df["Avg_S_score"].to_numpy()
    g_values = temp_df["Avg_G_score"].to_numpy()

    # E_score layer, bottom part
    ax.bar(
        x,
        e_values,
        width=bar_width,
        color=dimension_colours["E_score"],
        edgecolor="black",
        linewidth=0.4,
        alpha=0.90
    )

    # S_score layer, stacked on E_score
    ax.bar(
        x,
        s_values,
        width=bar_width,
        bottom=e_values,
        color=dimension_colours["S_score"],
        edgecolor="black",
        linewidth=0.4,
        alpha=0.90
    )

    # G_score layer, stacked on E_score + S_score
    ax.bar(
        x,
        g_values,
        width=bar_width,
        bottom=e_values + s_values,
        color=dimension_colours["G_score"],
        edgecolor="black",
        linewidth=0.4,
        alpha=0.90
    )

    # Add short category labels above each stacked bar
    total_values = e_values + s_values + g_values

    for x_pos, total_value in zip(x, total_values):
        ax.text(
            x_pos,
            total_value + 1.2,
            category_short_labels[category],
            ha="center",
            va="bottom",
            fontsize=7,
            rotation=90
        )

# 17. Axis settings
ax.set_title(
    "Yearly Average E, S, and G Score Composition by ESG Category",
    fontsize=17,
    fontweight="bold",
    pad=14
)

ax.set_xlabel(
    "Year Index (1 = 2015, 2 = 2016, ..., 8 = 2022)",
    fontsize=13
)

ax.set_ylabel("Average Score", fontsize=13)

ax.set_xticks(x_positions)
ax.set_xticklabels([str(i) for i in x_positions], fontsize=11)

ax.tick_params(axis="y", labelsize=11)

# 18. Set axis limits and grid
ax.set_xlim(0.45, len(years) + 0.55)

max_total_score = (
    group_average_df["Avg_E_score"]
    + group_average_df["Avg_S_score"]
    + group_average_df["Avg_G_score"]
).max()

ax.set_ylim(0, max_total_score * 1.16)

ax.grid(True, axis="y", linestyle="--", alpha=0.30)

# 19. Add explanatory note under x-axis
ax.text(
    0.5,
    -0.12,
    "Within each year: left = Top-tier, middle = Middle-tier, right = Bottom-tier",
    transform=ax.transAxes,
    ha="center",
    va="top",
    fontsize=10
)

# 20. Legends
dimension_handles = [
    Patch(
        facecolor=dimension_colours["E_score"],
        edgecolor="black",
        label="Average E_score"
    ),
    Patch(
        facecolor=dimension_colours["S_score"],
        edgecolor="black",
        label="Average S_score"
    ),
    Patch(
        facecolor=dimension_colours["G_score"],
        edgecolor="black",
        label="Average G_score"
    )
]

ax.legend(
    handles=dimension_handles,
    title="Stacked ESG Dimensions",
    loc="upper left",
    fontsize=10,
    title_fontsize=11,
    frameon=True
)

# 21. Save figure
fig.tight_layout()
fig.savefig(output_figure, dpi=300, bbox_inches="tight")
plt.close(fig)

# 22. Print summary
print("Layer 2 - Script 3 completed successfully.")
print(f"Saved figure: {output_figure}")
print("\nPreview of yearly E/S/G group averages:")
print(group_average_df[[
    "Year",
    "Year_Index",
    "ESG_Category",
    "Avg_E_score",
    "Avg_S_score",
    "Avg_G_score"
]].to_string(index=False))