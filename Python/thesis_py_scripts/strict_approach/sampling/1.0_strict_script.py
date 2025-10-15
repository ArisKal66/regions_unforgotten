import pandas as pd
import numpy as np
import fuzzywuzzy
from numpy import nan
from numpy import unique
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

dtypes = {'author23': str, 'author24': str, 'author25': str, 'author26': str}
df1_clean = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/df1_clean1.csv', sep = ';', dtype=dtypes)

df2 = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/lgbtq_base.csv')
df2['first_last_name'] = df2[['First Name','Last Name']].agg(' '.join, axis=1)

min_date = '1971-12-30'
APS_last_50yrs = df1_clean[df1_clean['date'] >= min_date].copy()

author_columns = [f'author{i}' for i in range(1, 27)]
APS_last_50yrs[author_columns] = APS_last_50yrs[author_columns].fillna('')
candidates_last_50yrs = np.unique(APS_last_50yrs[author_columns].values.flatten())

columns = ['input_value', 'match', 'score', 'ids', 'number_ids']

def find_best_matches_strict(APS_last_50yrs, candidates_last_50yrs, columns):
    result_df = pd.DataFrame(columns=columns)

    for index, row in df2.iterrows():
        value = row['first_last_name']
        matched_data = []
        for col in author_columns:
            best_matches = process.extract(value, candidates_last_50yrs, limit=10)
            for match, score in best_matches:
                ids = APS_last_50yrs[APS_last_50yrs[col] == match]['id'].values
                number_ids = len(ids)
                matched_data.append([value, match, score, ', '.join(ids), number_ids])
        match_df = pd.DataFrame(matched_data, columns=columns)
        result_df = pd.concat([result_df, match_df], ignore_index=True)

    return result_df

full_name_results = find_best_matches_strict(APS_last_50yrs, candidates_last_50yrs, columns)
full_name_results = full_name_results[full_name_results['score'] >= 96]
full_name_results = full_name_results.drop_duplicates()
full_name_results.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_fn_results.csv', sep=';', index=False)