import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/unique_loose96prc_researchers_nonC5.csv", sep=';')

def categorize_position(position):
    if pd.isna(position):
        return 'Unknown'
    position = position.lower()
    if 'postdoc' in position or 'post doc' in position:
        return 'Postdoc'
    elif 'professor' in position:
        return 'Professor'
    elif 'student' in position or 'phd' in position:
        return 'Student'
    elif 'research' in position or 'scientist' in position or 'physicist' in position:
        return 'Researcher'
    elif 'director' in position or 'dean' in position or 'ceo' in position or 'manager' in position or 'officer' in position:
        return 'Manager/Director'
    elif 'lecturer' in position or 'teacher' in position:
        return 'Lecturer/Teacher'
    else:
        return 'Other'

df['Position_Category'] = df['Position'].apply(categorize_position)

position_counts = df['Position_Category'].value_counts()

plt.figure(figsize=(10, 6))
bars = plt.bar(position_counts.index, position_counts.values, color='royalblue')
plt.xlabel('Position Category')
plt.ylabel('Number of Researchers')
plt.title('Distribution of LGBT Researchers by Position Category, with higher impact publ.')
plt.xticks(rotation=45, ha='right')  # Rotate labels for readability

# Add value counts on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.annotate(f'{height}', 
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),  # 3 points vertical offset
                 textcoords="offset points",
                 ha='center', va='bottom')

plt.tight_layout()  # Adjust layout to prevent labels from overlapping
plt.show()