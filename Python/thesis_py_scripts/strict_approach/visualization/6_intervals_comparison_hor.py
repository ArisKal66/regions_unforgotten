import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_lgbt = pd.read_csv("D:/Downloads/thesis/final/strict_appr/unique_strict_researchers.csv", sep=';')
df_lgbt['max_date_interval'] =pd.to_numeric(df_lgbt['max_date_interval'].astype(str).str.replace(',', '.'))
df_lgbt['max_min_interval'] =pd.to_numeric(df_lgbt['max_min_interval'].astype(str).str.replace(',', '.'))
# sub1 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_9_APS_subset_3_GA_all_papers.csv", sep=';')
# sub2 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_10_APS_subset_2_GA_all_papers.csv", sep=';')
# sub3 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_4_APS_subset_3_GA_all_papers.csv", sep=';')
# sub4 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_1_APS_subset_1_GA_all_papers.csv", sep=';')
# sub5 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/all_papers/Iter_4_APS_subset_2_GA_all_papers.csv", sep=';')

plt.figure(figsize=(12, 8))
# Function to add value counts with bin ranges on top of bars
def add_value_counts(ax, counts, bins):
    bin_centers = (bins[:-1] + bins[1:]) / 2
    for i, bar in enumerate(ax.patches):
        height = bar.get_height()
        bin_range = f'{bins[i]:.0f}-{bins[i+1]:.0f}'  # Changed to .0f for integer bin ranges
        ax.annotate(f'{int(height)}\n({bin_range})',
                    xy=(bin_centers[i], height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

# Plot for max_date_interval
ax1 = plt.subplot(1, 2, 1)
counts, bins, _ = ax1.hist(df_lgbt['max_date_interval'], bins=np.arange(0, df_lgbt['max_date_interval'].max() + 5, 5), alpha=0.5)
plt.xlabel('Time Since Last Publication (max_date_interval)')
plt.ylabel('Num. of Researchers')
plt.title('Distribution of Ages Since Last Publication')
plt.xticks(np.arange(0, int(df_lgbt['max_date_interval'].max()) + 1, 10))  # Ticks every 10 years
add_value_counts(ax1, counts, bins)  # Add value counts with bin ranges


# plt.subplot(2, 2, 3)  # Subplot for the table
# table_data = [['Bin Range', 'Count']]
# for i in range(len(bins) - 1):
#     bin_range = f'{bins[i]:.1f}-{bins[i+1]:.1f}'
#     table_data.append([bin_range, int(counts[i])])
# plt.table(cellText=table_data, loc='center', cellLoc='center')
# plt.axis('off')  # Hide axes for the table

# Plot for max_min_interval
ax2 = plt.subplot(1, 2, 2)
counts, bins, _ = ax2.hist(df_lgbt['max_min_interval'], bins=np.arange(0, df_lgbt['max_min_interval'].max() + 5, 5), alpha=0.5)  # Bins every 5 years
plt.xlabel('Career Stage (max_min_interval)')
plt.ylabel('Num. of Researchers')
plt.title('Distribution of Career Stage (in years)')
plt.xticks(np.arange(0, int(df_lgbt['max_min_interval'].max()) + 1, 10))  # Ticks every 10 years
add_value_counts(ax2, counts, bins)  # Add value counts with bin ranges

# plt.subplot(2, 2, 4)  # Subplot for the table
# table_data = [['Bin Range', 'Count']]
# for i in range(len(bins) - 1):
#     bin_range = f'{bins[i]:.1f}-{bins[i+1]:.1f}'
#     table_data.append([bin_range, int(counts[i])])
# plt.table(cellText=table_data, loc='center', cellLoc='center')
# plt.axis('off')  # Hide axes for the table

plt.tight_layout()
plt.show()