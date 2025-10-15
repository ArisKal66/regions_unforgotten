import pandas as pd
from scipy.stats import ttest_ind

# Paths
lgbtq_path = "D:/Downloads/thesis/final/strict_appr/unique_strict_researchers_nonC5.csv"
ga_base_path = "D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/"

# Files and fields
ga_files = [
    "Iter_2_APS_subset_2_GA_nonC5.csv",
    "Iter_2_APS_subset_1_GA_nonC5.csv",
    "Iter_5_APS_subset_2_GA_nonC5.csv",
    "Iter_3_APS_subset_5_GA_nonC5.csv",
    "Iter_8_APS_subset_1_GA_nonC5.csv"
]

# Field mapping
field_mapping = {
    'number_ids': 'number_ids',
    'sum_cc': 'sum_cc',
    'avg_cc': 'avg_cc',
    'sum_PagRank_score_inf': 'sum_pagerank_inf',
    'avg_PagRank_score_inf': 'avg_pagerank_inf',
    'sum_AttRank_score_pop': 'sum_attrank_pop',
    'avg_AttRank_score_pop': 'avg_attrank_pop',
    'sum_3year_cc_imp': 'sum_3year_cc_imp',
    'avg_3year_cc_imp': 'avg_3year_cc_imp'
}

# Fields that need fixing commas
fields_with_comma_issue = [
    'sum_PagRank_score_inf', 'avg_PagRank_score_inf',
    'sum_AttRank_score_pop', 'avg_AttRank_score_pop'
]

alpha = 0.05

# Load LGBTQ dataset
df_lgbtq = pd.read_csv(lgbtq_path, sep=';')

# Clean comma decimal for affected fields
for field in fields_with_comma_issue:
    if field in df_lgbtq.columns:
        df_lgbtq[field] = df_lgbtq[field].astype(str).str.replace(',', '.')
        
# Initialize list for results
results = []

# Loop through GA files
for ga_file in ga_files:
    ga_path = ga_base_path + ga_file
    df_ga = pd.read_csv(ga_path, sep=';')
    
    # Also fix commas for GA fields
    for _, ga_field in field_mapping.items():
        if ga_field in df_ga.columns and ga_field in [
            'sum_pagerank_inf', 'avg_pagerank_inf',
            'sum_attrank_pop', 'avg_attrank_pop'
        ]:
            df_ga[ga_field] = df_ga[ga_field].astype(str).str.replace(',', '.')
    
    # Loop through fields
    for lgbtq_field, ga_field in field_mapping.items():
        # Convert both fields to numeric (force errors to NaN and skip them)
        lgbtq_values = pd.to_numeric(df_lgbtq[lgbtq_field], errors='coerce')
        ga_values = pd.to_numeric(df_ga[ga_field], errors='coerce')
        
        # Drop NaNs
        lgbtq_values = lgbtq_values.dropna()
        ga_values = ga_values.dropna()
        
        # Perform t-test
        t_stat, p_value = ttest_ind(lgbtq_values, ga_values, equal_var=False)
        
        significance = "Significant" if p_value < alpha else "Not Significant"
        
        results.append({
            "GA_Subset_File": ga_file,
            "Field_Tested": lgbtq_field,
            "T-Statistic": t_stat,
            "P-Value": p_value,
            "Significance": significance
        })

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv("D:/Downloads/thesis/final/statistical_tests_results_fixed.csv", index=False, sep =";")

print("All tests done with corrected decimal points!")
