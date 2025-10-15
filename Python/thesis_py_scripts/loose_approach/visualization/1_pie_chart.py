import matplotlib.pyplot as plt

# Data
total_researchers = 775
matched_researchers = 364
high_impact_researchers = 296

# Calculate the number of researchers in each category
unmatched_researchers = total_researchers - matched_researchers
matched_low_impact_researchers = matched_researchers - high_impact_researchers

# Define labels and sizes for the pie chart
labels = ['Matched with high impact publ.', 'Matched', 'Unmatched']
sizes = [high_impact_researchers, matched_low_impact_researchers, unmatched_researchers]

# Define colors with good contrast and consider colorblindness
colors = ['teal', 'gold', 'silver']

# Create the pie chart with hatches for better accessibility
plt.figure(figsize=(8, 8))
wedges, _, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, 
                               textprops={'fontsize': 12}, wedgeprops={'linewidth': 1, 'edgecolor': 'black'})

# Add hatches for accessibility
hatches = ['//', 'oo', '..']
for i, wedge in enumerate(wedges):
    wedge.set_hatch(hatches[i])

# Add a title
plt.title('LGBT Researchers and Publication Impact')

# Ensure the circle's proportion
plt.axis('equal')

# Add a legend with clear labels
plt.legend(title='Researcher Group', loc='best')

# Modify labels to include both percentage and actual value with white background
for i, autotext in enumerate(autotexts):
    autotext.set_text(f'{autotext.get_text()} ({sizes[i]})')
    autotext.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

# Show the plot
plt.show()