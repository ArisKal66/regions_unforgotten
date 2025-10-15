import pandas as pd
import numpy as np
import fuzzywuzzy
from numpy import nan
from numpy import unique
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

dtypes = {'author23': str, 'author24': str, 'author25': str, 'author26': str}
df1_clean = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/df1_clean1.csv', sep = ';', dtype=dtypes)

min_date = '1971-12-30'
APS_last_50yrs = df1_clean[df1_clean['date'] >= min_date].copy()

author_columns = [f'author{i}' for i in range(1, 27)]

APS_last_50yrs[author_columns] = APS_last_50yrs[author_columns].fillna('')

df = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_fn_results.csv', sep=';')

def search_match(row):
    match = row['match']
    ids = []
    for col in author_columns:
        ids.extend(APS_last_50yrs.loc[APS_last_50yrs[col] == match, 'id'].tolist())
    return ', '.join(ids) if ids else '', len(ids)

df[['ids', 'number_ids']] = df.apply(search_match, axis=1, result_type='expand')

df.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_fn_results.csv', sep=';', index=False)