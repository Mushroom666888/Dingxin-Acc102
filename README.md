# ACC102 Individual Assignment: ESG Performance Classification and ROA Analysis of Indian Companies (2015–2022)

## 1. Project Background & Problem Statement

This project evaluates the relationship between ESG performance and financial performance among 22 major Indian companies from 2015 to 2022. As ESG factors have become increasingly important in business evaluation and investment decision-making, this project aims to classify firms based on their long-term ESG performance and examine whether different ESG groups show different ROA patterns.

The main analytical problem is to identify which companies demonstrate stronger ESG synergy, which companies remain at a standard ESG level, and which companies may face weaker ESG performance. The project also explores how ESG scores and ROA vary across these groups over time.

## 2. Data Description

The analysis uses a company-year ESG and financial dataset sourced from Bloomberg Terminal. The dataset covers 22 Indian companies over the period 2015–2022.

After data cleaning, this project keeps seven core variables:

- Year
- Company
- ESG_score
- E_score
- S_score
- G_score
- ROA

ESG_score represents the overall ESG performance. E_score, S_score, and G_score represent the environmental, social, and governance dimensions. ROA is used as the main financial performance indicator.

## 3. Methodology

The analysis follows a structured two-layer workflow.

### Layer 1: Data Cleaning and ESG Classification

The original Excel dataset is cleaned and reduced to seven core variables: Year, Company, ESG_score, E_score, S_score, G_score, and ROA.

A company-level weighted ESG indicator, Alpha_Weighted_ESG, is constructed using the eight-year average E_score, S_score, and G_score:

Alpha_Weighted_ESG = 0.4 × Avg_E_score + 0.4 × Avg_S_score + 0.2 × Avg_G_score

Based on this indicator, the 22 companies are classified into three ESG performance groups:

- Top-tier Synergy Leaders: Alpha_Weighted_ESG > 50
- Middle-tier Standard Group: 40 ≤ Alpha_Weighted_ESG ≤ 50
- Bottom-tier Social Traps: Alpha_Weighted_ESG < 40

Layer 1 produces one company-level ranking table and three classified company-year data tables.

### Layer 2: Visual Analysis

Layer 2 generates visual outputs to compare ESG performance and ROA across the three groups.

The first script creates ESG_score vs ROA scatter plots for each group. Each company-year observation is plotted as a point, and a group-level linear regression line is added as a reference trend.

The second script creates one dual-axis trend chart based on yearly group averages. Average ESG_score is shown using dashed lines on the left y-axis, while average ROA is shown using solid lines on the right y-axis.

The third script creates one grouped stacked bar chart. For each year, the three ESG groups are compared using stacked bars based on average E_score, S_score, and G_score.

## 4. Results & Key Findings

- The project classifies 22 companies into three ESG performance categories using a customised weighted ESG indicator.
- The Alpha_Weighted_ESG ranking identifies companies with stronger long-term ESG performance.
- The ESG_score vs ROA scatter plots show how profitability is distributed within each ESG group.
- The dual-axis trend chart compares the yearly average ESG_score and ROA of the three ESG categories from 2015 to 2022.
- The grouped stacked bar chart highlights the internal E, S, and G score composition of each ESG group over time.
- Overall, the project provides a structured way to compare ESG strength, ROA performance, and ESG dimension composition across different company groups.

## 5. How to Run

1. Clone or download this repository.

2. Make sure the project structure is organised as follows:

```text
ACC102_Track2_ESG_Project
│
├── data
│   └── esg_social_data.xlsx
│
├── outputs
│
├── layer1_esg_classification.py
├── layer2_esg_roa_scatter_fit.py
├── layer2_dual_axis_group_average_trend.py
└── layer2_esg_dimension_stacked_bar.py
```

3. Install the required Python packages:

```bash
pip install pandas numpy matplotlib openpyxl
```

4. Run the Python scripts in the following order:

```bash
python layer1_esg_classification.py
python layer2_esg_roa_scatter_fit.py
python layer2_dual_axis_group_average_trend.py
python layer2_esg_dimension_stacked_bar.py
```

5. The generated tables and figures will be saved in the `outputs` folder.

Layer 1 outputs include:

- layer1_company_alpha_ranking.csv
- layer1_top_tier_synergy_leaders.csv
- layer1_middle_tier_standard_group.csv
- layer1_bottom_tier_social_traps.csv

Layer 2 outputs include:

- ESG_score vs ROA scatter-fit figures
- One dual-axis yearly average ESG_score and ROA trend figure
- One grouped stacked bar chart of average E_score, S_score, and G_score

## 6. Product / Demo Links

Source Code: https://github.com/Mushroom666888/Dingxin-Acc102/tree/main/code

Generated Outputs: Included in the `outputs` folder of this repository.

## 7. Limitations & Future Improvements

Limitations: This analysis is limited to 22 Indian companies and covers only the period from 2015 to 2022. The classification method is based on a customised weighted ESG indicator, where E_score and S_score are given higher weights than G_score. Different weighting methods may lead to different classification results. In addition, ROA is the only financial performance variable used in the final analysis, so the project does not fully capture all aspects of financial performance.

Improvements: Future work could include more companies, more recent years, and additional financial indicators such as ROE, EBIT, or market-based performance measures. Further analysis could also include industry classification, regression models, and robustness checks to examine whether ESG performance is consistently associated with financial performance.
