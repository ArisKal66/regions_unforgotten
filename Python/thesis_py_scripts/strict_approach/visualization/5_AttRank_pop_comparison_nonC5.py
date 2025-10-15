import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_lgbt = pd.read_csv("D:/Downloads/thesis/final/strict_appr/unique_strict_researchers_nonC5.csv", sep=';')

sub1 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_2_APS_subset_2_GA_nonC5.csv", sep=';')
sub2 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_2_APS_subset_1_GA_nonC5.csv", sep=';')
sub3 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_5_APS_subset_2_GA_nonC5.csv", sep=';')
sub4 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_3_APS_subset_5_GA_nonC5.csv", sep=';')
sub5 = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets_GA/papers_nonE/Iter_8_APS_subset_1_GA_nonC5.csv", sep=';')

labels = ['LGBT Researchers', 'Subset1', 'Subset2', 'Subset3', 'Subset4', 'Subset5']
df = pd.read_csv("D:/Downloads/thesis/final/strict_appr/strict_subsets/GA_consol_metrics_nonC5.csv", sep=';')
colors = ['royalblue', 'wheat', 'seagreen', 'maroon', 'indigo', 'sienna']

dfs = [df_lgbt, sub1, sub2, sub3, sub4, sub5]

sum_pop = df['sum_AttRank_score_pop'].tolist()
sum_num_ids = df['number_ids_sum'].tolist()  # Get the sum of number_ids

plt.figure(figsize=(10, 6))

# Scatter plot with size based on number_ids_sum
x_coords = np.arange(len(labels))
for i in range(len(dfs)):
    plt.scatter(x_coords[i], sum_pop[i], s=sum_num_ids[i], label=labels[i], color=colors[i])
    if i == 3 or i == 4:
        color = 'white'
    else:
        color = 'black'
    
    plt.annotate(str(sum_num_ids[i]), (x_coords[i], sum_pop[i]),  # Add text annotation
                 textcoords="offset points", xytext=(0, 0), ha='center', color = color)

plt.xlabel('Dataset')
plt.ylabel('Popularity (AttRank Score)')
plt.title('Comparison of Popularity')
plt.xticks(x_coords, labels, rotation=45, ha='center')

# Get the handles and labels for the legend
handles, labels_legend = plt.gca().get_legend_handles_labels()

# Create a new legend with smaller, fixed-size markers
plt.legend(handles, labels_legend, markerscale=0.3)  # Adjust markerscale as needed

plt.tight_layout()
plt.show()