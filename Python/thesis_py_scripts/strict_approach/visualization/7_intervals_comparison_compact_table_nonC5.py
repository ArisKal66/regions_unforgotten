import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_lgbt = pd.read_csv("D:/Downloads/thesis/final/strict_appr/unique_strict_researchers_nonC5.csv", sep=';')
df_lgbt['max_date_interval'] =pd.to_numeric(df_lgbt['max_date_interval'].astype(str).str.replace(',', '.'))
df_lgbt['max_min_interval'] =pd.to_numeric(df_lgbt['max_min_interval'].astype(str).str.replace(',', '.'))
sub1 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_2_APS_subset_2_GA_nonC5.csv", sep=';')
sub1['max_date_interval'] =pd.to_numeric(sub1['max_date_interval'].astype(str).str.replace(',', '.'))
sub1['max_min_interval'] =pd.to_numeric(sub1['max_min_interval'].astype(str).str.replace(',', '.'))
sub2 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_2_APS_subset_1_GA_nonC5.csv", sep=';')
sub2['max_date_interval'] =pd.to_numeric(sub2['max_date_interval'].astype(str).str.replace(',', '.'))
sub2['max_min_interval'] =pd.to_numeric(sub2['max_min_interval'].astype(str).str.replace(',', '.'))
sub3 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_5_APS_subset_2_GA_nonC5.csv", sep=';')
sub3['max_date_interval'] =pd.to_numeric(sub3['max_date_interval'].astype(str).str.replace(',', '.'))
sub3['max_min_interval'] =pd.to_numeric(sub3['max_min_interval'].astype(str).str.replace(',', '.'))
sub4 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_3_APS_subset_5_GA_nonC5.csv", sep=';')
sub4['max_date_interval'] =pd.to_numeric(sub4['max_date_interval'].astype(str).str.replace(',', '.'))
sub4['max_min_interval'] =pd.to_numeric(sub4['max_min_interval'].astype(str).str.replace(',', '.'))
sub5 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_8_APS_subset_1_GA_nonC5.csv", sep=';')
sub5['max_date_interval'] =pd.to_numeric(sub5['max_date_interval'].astype(str).str.replace(',', '.'))
sub5['max_min_interval'] =pd.to_numeric(sub5['max_min_interval'].astype(str).str.replace(',', '.'))

# List of datasets and labels
dfs = [df_lgbt, sub1, sub2, sub3, sub4, sub5]
labels = ['LGBT Res.', 'Subset1', 'Subset2', 'Subset3', 'Subset4', 'Subset5']

# Function to create binned data for a DataFrame and metric
def create_binned_data(df, metric, bin_width=5):
    bins = np.arange(0, df[metric].max() + bin_width, bin_width)
    counts, _ = np.histogram(df[metric], bins=bins)
    bin_ranges = [f'{bins[i]:.0f}-{bins[i+1]:.0f}' for i in range(len(bins) - 1)]
    return dict(zip(bin_ranges, counts))



# Create the table data
table_data = [['Dataset'] + [f'{bin_range:.0f}-{bin_range+5:.0f} yrs' for bin_range in np.arange(0, 45, 5)] +
              [f'{bin_range}-{bin_range+5:.0f} yrs' for bin_range in np.arange(0, 50, 5)]]
for i, df in enumerate(dfs):
    row = [labels[i]]
    max_date_data = create_binned_data(df, 'max_date_interval')
    max_min_data = create_binned_data(df, 'max_min_interval')
    for bin_range in np.arange(0, 45, 5):
        row.append(max_date_data.get(f'{bin_range:.0f}-{bin_range+5:.0f}', '-'))
    for bin_range in np.arange(0, 50, 5):
        row.append(max_min_data.get(f'{bin_range:.0f}-{bin_range+5:.0f}', '-'))
    table_data.append(row)

# Create the table
fig, ax = plt.subplots(figsize=(12, 4))  # Adjust figsize as needed
extra_head = plt.table(cellText=[['']*2],
                       colLabels=['from last date of APS','Career Stage'],
                       loc = 'top'
                       )
ax.axis('off')
table = ax.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)  # Adjust fontsize as needed
table.scale(1.2, 1.2)  # Adjust scale as needed
plt.show()