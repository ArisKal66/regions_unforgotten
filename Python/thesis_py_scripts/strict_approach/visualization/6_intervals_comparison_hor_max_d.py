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

# plt.figure(figsize=(12, 8))

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

# Create subplots with shared x-axis
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig.subplots_adjust(hspace=0.05)

# Plot for max_date_interval on ax1
counts, bins, _ = ax1.hist(df_lgbt['max_date_interval'], bins=np.arange(0, df_lgbt['max_date_interval'].max() + 5, 5), alpha=0.5)
ax2.set_xlabel('Interval from Max APS date (years)')
ax1.set_ylabel('Num. of Researchers')
ax1.set_title('Distribution of Ages Since Last Publication')
add_value_counts(ax1, counts, bins)

# Plot for max_date_interval on ax2
counts, bins, _ = ax2.hist(df_lgbt['max_date_interval'], bins=np.arange(0, df_lgbt['max_date_interval'].max() + 5, 5), alpha=0.5)
add_value_counts(ax2, counts, bins)

# Set y-limits for the broken axis
ax1.set_ylim(140, 160)  # Outliers only
ax2.set_ylim(0, 40)  # Most of the data

# Hide the spines between ax1 and ax2
ax1.spines.bottom.set_visible(False)
ax2.spines.top.set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False)  # Don't put tick labels at the top
ax2.xaxis.tick_bottom()

# Add the cut-out slanted lines
d = 1
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

plt.show()