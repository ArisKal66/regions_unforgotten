import matplotlib.pyplot as plt

trgt_career = round(9.89512,2)
trgt_max_d = round(4.97988,2)
# Data from the log file
log_data = [
    ["File", "Trgt Career", "Avg career", "Diff career", "Trgt Max Date Int.", "Avg Max Date Int.", "Diff Max Date Int."],
    ["Iter_2_subset_2", trgt_career, round(9.91341,2), round(0.01829,2), trgt_max_d, round(5.31220,2), round(0.33232,2)],
    ["Iter_2_subset_1", trgt_career, round(9.93902,2), round(0.04390,2), trgt_max_d, round(5.77134,2), round(0.79146,2)],
    ["Iter_5_subset_2", trgt_career, round(9.95671,2), round(0.06159,2), trgt_max_d, round(5.34085,2), round(0.36098,2)],
    ["Iter_3_subset_5", trgt_career, round(9.83354,2), round(0.06159,2), trgt_max_d, round(5.47256,2), round(0.49268,2)],
    ["Iter_8_subset_1", trgt_career, round(9.79207,2), round(0.10305,2), trgt_max_d, round(5.62500,2), round(0.64512,2)]
]

# Create the table
fig, ax = plt.subplots(figsize=(10, 4))  # Adjust figsize as needed
ax.axis('off')
table = ax.table(cellText=log_data, loc='center', cellLoc='center')

plt.title('All Publications Publications: GA Prevalent Datasets strict', loc='center')
# Format the table
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)  # Adjust scale as needed

plt.show()