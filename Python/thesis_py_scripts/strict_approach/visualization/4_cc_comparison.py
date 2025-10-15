import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_lgbt = pd.read_csv("D:/Downloads/thesis/final/strict_appr/unique_strict_researchers.csv", sep=';')

sub1 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_9_APS_subset_3_GA_all_papers.csv", sep=';')
sub2 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_10_APS_subset_2_GA_all_papers.csv", sep=';')
sub3 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_4_APS_subset_3_GA_all_papers.csv", sep=';')
sub4 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_1_APS_subset_1_GA_all_papers.csv", sep=';')
sub5 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_4_APS_subset_2_GA_all_papers.csv", sep=';')

labels = ['LGBT Researchers', 'Subset1', 'Subset2', 'Subset3', 'Subset4', 'Subset5']
df = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets/GA_consol_metrics_all_papers.csv", sep=';')

dfs = [df_lgbt, sub1, sub2, sub3, sub4, sub5]

plt.figure(figsize=(10, 6))
bar_width = 0.15
index = np.arange(len(labels))

sum_cc_sums = df['sum_cc_sum'].tolist()

patterns = ['/', '\\', '|', '-', '+', 'x']

for i in range(len(dfs)):
    bar = plt.bar(index[i] + bar_width, sum_cc_sums[i], bar_width, label=labels[i])
    bar[0].set_hatch(patterns[i])  # Set the pattern for each bar

    # Add value counts on top of each bar
    height = bar[0].get_height()
    plt.annotate(f'{height}',
                 xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                 xytext=(0, 3),  # 3 points vertical offset
                 textcoords="offset points",
                 ha='center', va='bottom')

plt.xlabel('Datasets')
plt.ylabel('Total Citation Count')
plt.title('Strict Results: Comparison of Total Citation Count on all publications')
plt.xticks(index + bar_width * (len(dfs) - 1) / 2, labels, rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()