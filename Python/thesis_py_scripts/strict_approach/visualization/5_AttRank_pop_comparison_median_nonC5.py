import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_lgbt = pd.read_csv("D:/Downloads/thesis/final/strict_appr/unique_strict_researchers_nonC5.csv", sep=';')
df_lgbt['sum_AttRank_score_pop'] = df_lgbt['sum_AttRank_score_pop'].astype(str).str.replace(',', '.').astype(float)
lgbt_pop = df_lgbt['sum_AttRank_score_pop'].sort_values()

sub1 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_2_APS_subset_2_GA_nonC5.csv", sep=';')
sub1['sum_attrank_pop'] = sub1['sum_attrank_pop'].astype(str).str.replace(',', '.').astype(float)
sub1_pop = sub1['sum_attrank_pop'].sort_values()
sub2 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_2_APS_subset_1_GA_nonC5.csv", sep=';')
sub2['sum_attrank_pop'] = sub2['sum_attrank_pop'].astype(str).str.replace(',', '.').astype(float)
sub2_pop = sub1['sum_attrank_pop'].sort_values()
sub3 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_5_APS_subset_2_GA_nonC5.csv", sep=';')
sub3['sum_attrank_pop'] = sub3['sum_attrank_pop'].astype(str).str.replace(',', '.').astype(float)
sub3_pop = sub1['sum_attrank_pop'].sort_values()
sub4 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_3_APS_subset_5_GA_nonC5.csv", sep=';')
sub4['sum_attrank_pop'] = sub4['sum_attrank_pop'].astype(str).str.replace(',', '.').astype(float)
sub4_pop = sub1['sum_attrank_pop'].sort_values()
sub5 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_8_APS_subset_1_GA_nonC5.csv", sep=';')
sub5['sum_attrank_pop'] = sub5['sum_attrank_pop'].astype(str).str.replace(',', '.').astype(float)
sub5_pop = sub1['sum_attrank_pop'].sort_values()

labels = ['LGBT Researchers', 'Subset1', 'Subset2', 'Subset3', 'Subset4', 'Subset5']

popularity_values = [
    df_lgbt['sum_AttRank_score_pop'],
    sub1['sum_attrank_pop'],
    sub2['sum_attrank_pop'],
    sub3['sum_attrank_pop'],
    sub4['sum_attrank_pop'],
    sub5['sum_attrank_pop']
]


outlier_counts = []

# Calculate outliers and whisker values
for dataset in popularity_values:
    q1 = np.percentile(dataset.dropna(), 25)  # First quartile
    q3 = np.percentile(dataset.dropna(), 75)  # Third quartile
    iqr = q3 - q1  # Interquartile range
    lower_whisker = q1 - 1.5 * iqr
    upper_whisker = q3 + 1.5 * iqr
    
    # Count outliers
    outliers = dataset[(dataset < lower_whisker) | (dataset > upper_whisker)]
    outlier_counts.append(len(outliers))

# Create the box plot
plt.figure(figsize=(10, 6))
box = plt.boxplot(
    popularity_values,
    labels=labels,
    patch_artist=True,
    showmeans=True,
    showfliers=False  # Do not show outliers
)

# Customize the appearance of the box plot
colors = ['royalblue', 'wheat', 'seagreen', 'maroon', 'indigo', 'sienna']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Highlight the median lines
for median in box['medians']:
    median.set_color('black')
    median.set_linewidth(3)

# Add the count of excluded outliers as annotations
for i, count in enumerate(outlier_counts):
    plt.text(
        i + 1,  # Position at the center of the box (x-axis)
        box['caps'][2 * i + 1].get_ydata()[0] + 0.05,  # Slightly above the upper whisker
        f'Outliers: {count}', 
        ha='center', 
        fontsize=10, 
        color='blue'
    )

# Customize the plot
plt.title('BoxPlots of Popularity Scores Across Datasets', fontsize=14)
plt.ylabel('Popularity Score', fontsize=12)
plt.xlabel('Datasets', fontsize=12)
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()