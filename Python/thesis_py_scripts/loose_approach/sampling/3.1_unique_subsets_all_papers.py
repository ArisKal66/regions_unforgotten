import pandas as pd
import numpy as np
from datetime import datetime

# Function to log timestamps
def log_time(message):
    print(f"{message} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Define author columns and data types
author_columns = [f'author{i}' for i in range(1, 27)]
dtypes = {'author23': str, 'author24': str, 'author25': str, 'author26': str}

# Load datasets
APS_last_50yrs = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/APS_last_50yrs.csv', sep=';', dtype=dtypes)
APS_last_50yrs[author_columns] = APS_last_50yrs[author_columns].fillna('')
APS_last_50yrs['id'] = APS_last_50yrs['id'].str.lower()

# Convert date column to datetime
APS_last_50yrs['date'] = pd.to_datetime(APS_last_50yrs['date'])

APS_CC = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/files_20240627/APS-CC_topics.csv', sep='\t')

# Merge APS_CC into APS_last_50yrs
APS_last_50yrs = APS_last_50yrs.merge(APS_CC, how='left', left_on='id', right_on='doi')
APS_last_50yrs.drop(columns='doi', inplace=True)

loose96_paper_ids = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose96prc_paper_ids.csv', sep=';')

long_authors = APS_last_50yrs.melt(
    id_vars=['id', 'date'],  # Include only necessary columns for this step
    value_vars=author_columns,
    var_name='author_column',
    value_name='author_name'
)

long_authors = long_authors[long_authors['author_name'] != '']

matches_to_exclude = pd.concat(
    [loose96_paper_ids['match1'], loose96_paper_ids['match2'], loose96_paper_ids['match3']]
).dropna()  # Combine match1, match2 and match3, dropping NaN values

long_authors = long_authors[~long_authors['author_name'].isin(matches_to_exclude)]
log_time("Exclusion of strict paper IDs (match1,2 and 3) completed")

long_authors = long_authors[~long_authors['author_name'].str.match(r'^[\W0-9]', na=False)]
log_time("Removed faulty rows with special characters or numbers")

result_df = (
    long_authors.groupby('author_name')
    .agg(
        number_ids=('id', 'nunique'),
        max_date=('date', 'max'),
        min_date=('date', 'min')
    )
    .reset_index()
)

# Calculate additional fields: max_date_interval and max_min_interval
result_df['max_date_interval'] = round(
    (pd.to_datetime('2021-12-30') - result_df['max_date']).dt.days / 365.242, 1
)
result_df['max_min_interval'] = round(
    (result_df['max_date'] - result_df['min_date']).dt.days / 365.242, 1
)

# Filter results based on valid number_ids
result_df = result_df[result_df['number_ids'] > 0]

result_df.to_csv(
    '/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/filtered_candidates_96prc_all_papers.csv',
    sep=';',
    index=False
)
log_time("Result CSV saved")