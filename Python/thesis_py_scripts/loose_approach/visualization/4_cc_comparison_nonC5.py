import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 
df_lgbt = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/unique_loose96prc_researchers_nonC5.csv", sep=';')

sub1 = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/loose_subsets_GA/papers_nonE/Iter_10_APS_subset_4_GA_nonC5.csv", sep=';')
sub2 = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/loose_subsets_GA/papers_nonE/Iter_3_APS_subset_3_GA_nonC5.csv", sep=';')
sub3 = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/loose_subsets_GA/papers_nonE/Iter_7_APS_subset_5_GA_nonC5.csv", sep=';')
sub4 = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/loose_subsets_GA/papers_nonE/Iter_4_APS_subset_2_GA_nonC5.csv", sep=';')
sub5 = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/loose_subsets_GA/papers_nonE/Iter_5_APS_subset_4_GA_nonC5.csv", sep=';')

labels = ['LGBT Researchers', 'Subset1', 'Subset2', 'Subset3', 'Subset4', 'Subset5']
df = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/96prc_subsets/GA_consol_metrics_nonC5.csv", sep=';')
colors = ['royalblue', 'wheat', 'seagreen', 'maroon', 'indigo', 'sienna']

dfs = [df_lgbt, sub1, sub2, sub3, sub4, sub5]

plt.figure(figsize=(10, 6))
bar_width = 0.30
index = np.arange(len(labels))

sum_cc_sums = df['sum_cc_sum'].tolist()

patterns = ['/', '\\', '|', '-', '+', 'x']

for i in range(len(dfs)):
    bar = plt.bar(index[i] + bar_width, sum_cc_sums[i], bar_width, label=labels[i], color=colors[i])
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
plt.title('Loose 96prc Results: Comparison of Total Citation Count on higher impact publications')
plt.xticks(index + bar_width * (len(dfs) - 1) / 2, labels, rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()