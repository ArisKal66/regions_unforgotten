import pandas as pd

author_columns = [f'author{i}' for i in range(1, 27)]
dtypes = {'author23': str, 'author24': str, 'author25': str, 'author26': str}
APS_last_50yrs = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/APS_last_50yrs.csv', sep=';', dtype=dtypes)
APS_last_50yrs[author_columns] = APS_last_50yrs[author_columns].fillna('')
APS_last_50yrs['id'] = APS_last_50yrs['id'].str.lower()

dtypes_aps = {'cc': 'Int64', '3year_cc_imp': 'Int64', 'PagRank_score_inf': float, 'AttRank_score_pop': float}
APS_CC = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/files_20240627/APS-CC_topics.csv',sep = '\t', dtype=dtypes_aps)

APS_last_50yrs = APS_last_50yrs.merge(APS_CC, how='left', left_on='id', right_on='doi')
APS_last_50yrs.drop(columns='doi', inplace=True)

filtered_candidates = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/filtered_candidates.csv', sep=';')
filtered_candidates = filtered_candidates.rename(columns={"author_name": "input_value"})

long_authors = APS_last_50yrs.melt(
    id_vars=['id', 'cc', 'PagRank_score_inf', 'AttRank_score_pop', '3year_cc_imp'],
    value_vars=author_columns,
    var_name='author_column',
    value_name='author_name'
)

print("long authors created")

# Drop empty author names to reduce unnecessary rows
long_authors = long_authors[long_authors['author_name'] != '']

# Merge filtered_candidates with long_authors on the input_value and author_name
matches = filtered_candidates.merge(
    long_authors,
    how='left',
    left_on='input_value',
    right_on='author_name'
)

print("matches created")

# Group by input_value and aggregate the required fields
results_df = matches.groupby('input_value').agg(
    ids=('id', lambda x: ','.join(x.dropna().unique())),
    sum_cc =('cc', 'sum'),
    avg_cc =('cc', 'mean'),
    sum_pagerank_inf=('PagRank_score_inf', 'sum'),
    avg_pagerank_inf=('PagRank_score_inf', 'mean'),
    sum_attrank_pop=('AttRank_score_pop', 'sum'),
    avg_attrank_pop=('AttRank_score_pop', 'mean'),
    sum_3year_cc_imp=('3year_cc_imp', 'sum'),
    avg_3year_cc_imp=('3year_cc_imp', 'mean')
).reset_index()

# Save the results to a CSV
results_df.to_csv(
    '/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/filtered_candidates_metadata.csv', 
    sep=';', 
    index=False
)

print("done!")