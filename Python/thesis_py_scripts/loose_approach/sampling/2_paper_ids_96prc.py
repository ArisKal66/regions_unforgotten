import pandas as pd
import numpy as np

# Load the filtered results
results = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc_filtered.csv', sep=';')
results['ids'] = results['ids'].str.lower()  # Standardize IDs to lowercase

# Prepare a list to hold the processed rows
dfs = []

# Process each row in the results DataFrame
for index, row in results.iterrows():
    # Split the IDs into individual DOI entries
    ids = [id.strip() for id in row['ids'].split(',')]

    # Loop through the IDs and matches
    for idx, id in enumerate(ids):
        matches = [row.get(f'match{i + 1}', np.nan) for i in range(3)]  # Extract match1, match2, match3
        scores = [row.get(f'score{i + 1}', np.nan) for i in range(3)]  # Extract score1, score2, score3

        # Create a DataFrame for the current ID
        df = pd.DataFrame({
            'researcher_id': [row['researcher_id']],
            'ids': [id],
            'number_ids': [row['number_ids']],
            'match1': [matches[0]],
            'match2': [matches[1]],
            'match3': [matches[2]],
            'score1': [scores[0]],
            'score2': [scores[1]],
            'score3': [scores[2]],
            'max_date': [row['max_date']],
            'min_date': [row['min_date']],
            'max_date_interval': [row['max_date_interval']],
            'max_min_interval': [row['max_min_interval']]
        })

        dfs.append(df)

# Combine all processed rows into a single DataFrame
loose96prc_paper_ids = pd.concat(dfs, ignore_index=True)

# Load APS-CC metadata and merge with the results
APS_CC = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/files_20240627/APS-CC_topics.csv', sep='\t')

# Merge the results with APS-CC
loose96prc_paper_ids = pd.merge(loose96prc_paper_ids, APS_CC, left_on='ids', right_on='doi', how='left')
loose96prc_paper_ids['cc'] = pd.to_numeric(loose96prc_paper_ids['cc'], errors='coerce', downcast='integer')
loose96prc_paper_ids.drop(columns='doi', inplace=True)  # Drop the duplicate DOI column
loose96prc_paper_ids['cc'].fillna(0, inplace=True)

# Load APS metadata for the last 50 years and merge with results
dtypes = {'author23': str, 'author24': str, 'author25': str, 'author26': str}
APS_last_50yrs = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/APS_last_50yrs.csv', sep=';', dtype=dtypes)
APS_last_50yrs['id'] = APS_last_50yrs['id'].str.lower()  # Standardize IDs to lowercase

# Merge the results with APS_last_50yrs
loose96prc_paper_ids = pd.merge(loose96prc_paper_ids, APS_last_50yrs, left_on='ids', right_on='id', how='left')
loose96prc_paper_ids.drop(columns='id', inplace=True)  # Drop duplicate ID column
loose96prc_paper_ids['date'] = pd.to_datetime(loose96prc_paper_ids['date'])

grouped = loose96prc_paper_ids.groupby('researcher_id').agg(
    max_date=('date', 'max'),
    min_date=('date', 'min')
).reset_index()

loose96prc_paper_ids = loose96prc_paper_ids.merge(grouped, on='researcher_id', how = 'left')
loose96prc_paper_ids = loose96prc_paper_ids.rename(columns={'max_date_x': 'max_date', 'min_date_x': 'min_date'})
loose96prc_paper_ids.drop(columns={'max_date_y', 'min_date_y'}, inplace=True)
loose96prc_paper_ids.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose96prc_paper_ids.csv', sep=';', index=False)

# Calculate the sum and average of PagRank_score_inf and AttRank_score_pop for unique researchers
metrics = loose96prc_paper_ids.groupby('researcher_id').agg(
    sum_cc=('cc', 'sum'),
    avg_cc=('cc', 'mean'),
    sum_PagRank_score_inf=('PagRank_score_inf', 'sum'),
    avg_PagRank_score_inf=('PagRank_score_inf', 'mean'),
    sum_AttRank_score_pop=('AttRank_score_pop', 'sum'),
    avg_AttRank_score_pop=('AttRank_score_pop', 'mean'),
    sum_3year_cc_imp=('3year_cc_imp', 'sum'),
    avg_3year_cc_imp=('3year_cc_imp', 'mean')
).reset_index()

unique_loose96prc_researchers = results.drop_duplicates()
unique_loose96prc_researchers = unique_loose96prc_researchers.merge(metrics, on='researcher_id', how='left')
unique_loose96prc_researchers.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/unique_loose96prc_researchers.csv', sep=';', index=False)

# Filter non-C5 papers and create separate datasets
loose96prc_paper_ids_nonC5 = loose96prc_paper_ids[
    loose96prc_paper_ids['five_point_class'].notna() & (loose96prc_paper_ids['five_point_class'] != 'C5')
]

grouped_nonC5 = loose96prc_paper_ids_nonC5.groupby('researcher_id').agg(
    number_ids=('ids', 'count')
).reset_index()

loose96prc_paper_ids_nonC5 = loose96prc_paper_ids_nonC5.merge(grouped_nonC5, on='researcher_id', how='left')
loose96prc_paper_ids_nonC5 = loose96prc_paper_ids_nonC5.rename(columns={'number_ids_y': 'number_ids_nonC5'})
loose96prc_paper_ids_nonC5.drop(columns='number_ids_x', inplace=True)
loose96prc_paper_ids_nonC5.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose96prc_paper_ids_nonC5.csv', sep=';', index=False)

# Calculate the sum and average of PagRank_score_inf and AttRank_score_pop for unique non-C5 researchers
metrics_nonC5 = loose96prc_paper_ids_nonC5.groupby('researcher_id').agg(
    sum_cc =('cc', 'sum'),
    avg_cc =('cc', 'mean'),
    sum_PagRank_score_inf=('PagRank_score_inf', 'sum'),
    avg_PagRank_score_inf=('PagRank_score_inf', 'mean'),
    sum_AttRank_score_pop=('AttRank_score_pop', 'sum'),
    avg_AttRank_score_pop=('AttRank_score_pop', 'mean'),
    sum_3year_cc_imp=('3year_cc_imp', 'sum'),
    avg_3year_cc_imp=('3year_cc_imp', 'mean')
).reset_index()

unique_loose96prc_researchers_nonC5 = results.drop_duplicates()
unique_loose96prc_researchers_nonC5 = unique_loose96prc_researchers_nonC5.merge(metrics_nonC5, on='researcher_id', how='left')

columns_to_check = [
    'sum_cc', 'avg_cc', 'sum_PagRank_score_inf', 'avg_PagRank_score_inf',
    'sum_AttRank_score_pop', 'avg_AttRank_score_pop', 'sum_3year_cc_imp', 'avg_3year_cc_imp'
]

unique_loose96prc_researchers_nonC5 = unique_loose96prc_researchers_nonC5.dropna(subset=columns_to_check, how='any')

valid_ids = loose96prc_paper_ids_nonC5.groupby('researcher_id')['ids'].apply(
    lambda x: ', '.join(x)
).reset_index()

valid_ids.rename(columns={'ids': 'valid_ids'}, inplace=True)

unique_loose96prc_researchers_nonC5 = unique_loose96prc_researchers_nonC5.merge(
    valid_ids, on='researcher_id', how='left'
)

unique_loose96prc_researchers_nonC5['number_ids'] = unique_loose96prc_researchers_nonC5['valid_ids'].apply(
    lambda x: len(x.split(', ')) if pd.notna(x) else 0
)

unique_loose96prc_researchers_nonC5['ids'] = unique_loose96prc_researchers_nonC5['valid_ids']
unique_loose96prc_researchers_nonC5.drop(columns=['valid_ids'], inplace=True)
unique_loose96prc_researchers_nonC5.drop_duplicates()

unique_loose96prc_researchers_nonC5.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/unique_loose96prc_researchers_nonC5.csv', sep=';', index=False)

print("Processing complete. Results saved.")