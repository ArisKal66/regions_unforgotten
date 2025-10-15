import matplotlib.pyplot as plt

trgt_career = round(9.89512,2)
trgt_max_d = round(4.97988,2)
# Data from the log file
log_data = [
    ["File", "Trgt Career", "Avg career", "Diff career", "Trgt Max Date Int.", "Avg Max Date Int.", "Diff Max Date Int."],
    ["Iter_2_subset_3", trgt_career, round(10.14390,2), round(0.24878,2), trgt_max_d, round(6.07195,2), round(1.09207,2)],
    ["Iter_1_subset_1", trgt_career, round(9.60488,2), round(0.29024,2), trgt_max_d, round(6.01646,2), round(1.03659,2)],
    ["Iter_7_subset_5", trgt_career, round(9.49756,2), round(0.39756,2), trgt_max_d, round(6.12256,2), round(1.14268,2)],
    ["Iter_1_subset_4", trgt_career, round(9.46463,2), round(0.43049,2), trgt_max_d, round(6.03476,2), round(1.05488,2)],
    ["Iter_6_subset_1", trgt_career, round(9.44390,2), round(0.45122,2), trgt_max_d, round(6.07012,2), round(1.09024,2)]
]

# Create the table
fig, ax = plt.subplots(figsize=(10, 4))  # Adjust figsize as needed
ax.axis('off')
table = ax.table(cellText=log_data, loc='center', cellLoc='center')

plt.title('Higher Impact Publications: Heuristic Prevalent Datasets strict', loc='center')
# Format the table
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)  # Adjust scale as needed

plt.show()