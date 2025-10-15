import pandas as pd
import numpy as np
from numpy import nan
from numpy import unique

results = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_fn_results.csv', sep=';')
results['ids'] = results['ids'].str.lower()

dfs = []

for index, row in results.iterrows():
    ids = [id.strip() for id in row['ids'].split(',')]

    for idx, id in enumerate(ids):
        matches = [row.get(f'match{i + 1}', np.nan) for i in range(2)]  # Extract match1, match2
        scores = [row.get(f'score{i + 1}', np.nan) for i in range(2)]  # Extract score1, score2

        # Create a DataFrame for the current ID
        df = pd.DataFrame({
            'researcher_id': [row['researcher_id']],
            'input_value': [row['input_value']],
            'ids': [id],
            'number_ids': [row['number_ids']],
            'match1': [matches[0]],
            'match2': [matches[1]],
            'score1': [scores[0]],
            'score2': [scores[1]]
        })

        dfs.append(df)

strict_paper_ids = pd.concat(dfs, ignore_index=True)

APS_CC = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/files_20240627/APS-CC_topics.csv',sep = '\t')

strict_paper_ids = pd.merge(strict_paper_ids, APS_CC, left_on='ids', right_on='doi', how='left')
strict_paper_ids['cc'] = pd.to_numeric(strict_paper_ids['cc'], errors='coerce', downcast='integer')
strict_paper_ids.drop(columns='doi', inplace=True)
strict_paper_ids['cc'].fillna(0, inplace=True)

dtypes = {'author23': str, 'author24': str, 'author25': str, 'author26': str}
APS_last_50yrs = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/APS_last_50yrs.csv', sep=';', dtype=dtypes)
APS_last_50yrs['id'] = APS_last_50yrs['id'].str.lower()

strict_paper_ids = pd.merge(strict_paper_ids, APS_last_50yrs, left_on='ids', right_on='id', how='left')
strict_paper_ids.drop(columns='id', inplace=True)
strict_paper_ids['date'] = pd.to_datetime(strict_paper_ids['date'])

grouped = strict_paper_ids.groupby('input_value').agg(
    max_date=('date', 'max'),
    min_date=('date', 'min')
).reset_index()

strict_paper_ids = strict_paper_ids.merge(grouped, on='input_value', how='left')
strict_paper_ids['max_date_interval'] = round((pd.to_datetime('2021-12-30') - strict_paper_ids['max_date']).dt.days/365.242, ndigits=1)
strict_paper_ids['max_min_interval'] = round((strict_paper_ids['max_date'] - strict_paper_ids['min_date']).dt.days/365.242, ndigits=1)
strict_paper_ids.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_paper_ids.csv', sep=';', index=False)

metrics = strict_paper_ids.groupby('input_value').agg(
    sum_cc =('cc', 'sum'),
    avg_cc =('cc', 'mean'),
    sum_PagRank_score_inf=('PagRank_score_inf', 'sum'),
    avg_PagRank_score_inf=('PagRank_score_inf', 'mean'),
    sum_AttRank_score_pop=('AttRank_score_pop', 'sum'),
    avg_AttRank_score_pop=('AttRank_score_pop', 'mean'),
    sum_3year_cc_imp=('3year_cc_imp', 'sum'),
    avg_3year_cc_imp=('3year_cc_imp', 'mean')
).reset_index()

unique_strict_researchers = results.drop_duplicates()
unique_strict_researchers = unique_strict_researchers.drop_duplicates(subset=['researcher_id', 'input_value', 'ids'])
unique_strict_researchers = unique_strict_researchers.merge(metrics, on='input_value', how='left')
info_needed = strict_paper_ids[['researcher_id','max_date','min_date','max_date_interval','max_min_interval']]
info_needed = info_needed.rename(columns={'researcher_id':'res_id'})
unique_strict_researchers = pd.merge(unique_strict_researchers, info_needed, left_on='researcher_id', right_on='res_id', how='left')
unique_strict_researchers.drop(columns='res_id', inplace=True)
unique_strict_researchers.drop_duplicates()
unique_strict_researchers.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers.csv', sep=';', index=False)

strict_paper_ids_nonE = strict_paper_ids[strict_paper_ids['five_point_class'].notna() & (strict_paper_ids['five_point_class'] != 'C5')]

grouped_nonE = strict_paper_ids_nonE.groupby('input_value').agg(
    number_ids = ('ids', 'count')
).reset_index()

strict_paper_ids_nonE = strict_paper_ids_nonE.merge(grouped_nonE, on='input_value', how='left')
strict_paper_ids_nonE = strict_paper_ids_nonE.drop(columns='number_ids_x')
strict_paper_ids_nonE = strict_paper_ids_nonE.rename(columns={'number_ids_y': 'number_ids'})
strict_paper_ids_nonE.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_paper_ids_nonC5.csv', sep=';', index=False)

metrics_nonC5 = strict_paper_ids_nonE.groupby('input_value').agg(
    sum_cc =('cc', 'sum'),
    avg_cc =('cc', 'mean'),
    sum_PagRank_score_inf=('PagRank_score_inf', 'sum'),
    avg_PagRank_score_inf=('PagRank_score_inf', 'mean'),
    sum_AttRank_score_pop=('AttRank_score_pop', 'sum'),
    avg_AttRank_score_pop=('AttRank_score_pop', 'mean'),
    sum_3year_cc_imp=('3year_cc_imp', 'sum'),
    avg_3year_cc_imp=('3year_cc_imp', 'mean')
).reset_index()

unique_strict_researchers_nonE = results.drop_duplicates()
unique_strict_researchers_nonE = unique_strict_researchers_nonE.drop_duplicates(subset=['researcher_id', 'input_value', 'ids'])
unique_strict_researchers_nonE = unique_strict_researchers_nonE.merge(metrics_nonC5, on ='input_value', how = 'left')
unique_strict_researchers_nonE = pd.merge(unique_strict_researchers_nonE, info_needed, left_on='researcher_id', right_on='res_id', how='left')
unique_strict_researchers_nonE.drop(columns='res_id', inplace=True)

columns_to_check = [
    'sum_cc', 'avg_cc', 'sum_PagRank_score_inf', 'avg_PagRank_score_inf',
    'sum_AttRank_score_pop', 'avg_AttRank_score_pop', 'sum_3year_cc_imp', 'avg_3year_cc_imp'
]

unique_strict_researchers_nonE = unique_strict_researchers_nonE.dropna(subset=columns_to_check, how='any')

valid_ids = strict_paper_ids_nonE.groupby('input_value')['ids'].apply(
    lambda x: ', '.join(x)
).reset_index()

valid_ids.rename(columns={'ids': 'valid_ids'}, inplace=True)

# Merge the valid IDs back into the researchers DataFrame
unique_strict_researchers_nonE = unique_strict_researchers_nonE.merge(
    valid_ids, on='input_value', how='left'
)

# Count the number of IDs in the `valid_ids` column
unique_strict_researchers_nonE['number_ids'] = unique_strict_researchers_nonE['valid_ids'].apply(
    lambda x: len(x.split(', ')) if pd.notna(x) else 0
)

#Replace the `ids` column with the updated `valid_ids`
unique_strict_researchers_nonE['ids'] = unique_strict_researchers_nonE['valid_ids']
unique_strict_researchers_nonE.drop(columns=['valid_ids'], inplace=True)
unique_strict_researchers_nonE.drop_duplicates()
unique_strict_researchers_nonE.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers_nonC5.csv', sep=';', index=False)