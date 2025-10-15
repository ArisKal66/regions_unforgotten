import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

df_lgbtq = pd.read_csv("D:/Downloads/thesis/final/strict_appr/unique_strict_researchers_nonC5.csv", sep = ';')
GA_sub = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_2_APS_subset_2_GA_nonC5.csv", sep = ';')

df_lgbtq_param1 = df_lgbtq['number_ids']
GA_sub_param1 = GA_sub['number_ids']

t_stat, p_value = ttest_ind(df_lgbtq_param1, GA_sub_param1, equal_var= False)

alpha = 0.05  # Significance level

print(f"T-Statistic: {t_stat}")
print(f"P-Value: {p_value}")

if p_value < alpha:
    print("Reject the null hypothesis: There is a significant difference between the two groups.")
else:
    print("Fail to reject the null hypothesis: No significant difference found.")