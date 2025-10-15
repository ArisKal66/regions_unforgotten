import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("D:/Downloads/thesis/final/loose_appr/96prc/loose96prc_paper_ids_nonC5.csv", sep=';')

all_topics = pd.concat([df['topic1'], df['topic2'], df['topic3']])

topic_counts = all_topics.dropna().value_counts()

plt.figure(figsize=(12, 8))
topic_counts[:20].plot(kind='barh', color='skyblue')
plt.xlabel('Number of Publications')
plt.ylabel('Topics')
plt.title('Distribution of Topics in Publications by LGBT Researchers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()