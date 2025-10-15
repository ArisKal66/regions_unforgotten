import pandas as pd
from datetime import datetime

# Constants
max_dateAPS = datetime.strptime('2021-12-30', '%Y-%m-%d')
min_date = '1971-12-30'
year_days = 365.242

# File paths
filtered_file_path = '/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc_filtered.csv' # Change
outliers_file_path = '/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/96prc_outliers.csv' # Change
df1_clean_path = '/data2/aris/metadata/aps-dataset-metadata-2021/df1_clean1.csv'

# Load data
filtered_results = pd.read_csv(filtered_file_path, sep=';')
outliers = pd.read_csv(outliers_file_path, sep=';')
author_columns = [f'author{i}' for i in range(1, 27)]
dtypes = {col: str for col in author_columns}
df1_clean = pd.read_csv(df1_clean_path, sep=';', dtype=dtypes)

# Preprocess datasets
df1_clean = df1_clean[df1_clean['date'] >= min_date].copy()
df1_clean['id'] = df1_clean['id'].str.lower()
df1_clean['date'] = pd.to_datetime(df1_clean['date'], format='%Y-%m-%d')
df1_clean[author_columns] = df1_clean[author_columns].fillna('')
for col in author_columns:
    df1_clean[col] = df1_clean[col].str.replace('.', '', regex=False)

filtered_results['max_date'] = pd.to_datetime(filtered_results['max_date'], format='%Y-%m-%d')
filtered_results['min_date'] = pd.to_datetime(filtered_results['min_date'], format='%Y-%m-%d')

# Create a set of outlier researcher_id-match pairs for fast filtering
outlier_pairs = set(outliers.itertuples(index=False, name=None))

# Parse outliers into a dictionary {researcher_id: [list of matches to omit]}
outlier_dict = (
    outliers.groupby('researcher_id')['match']
    .apply(list)
    .to_dict()
)

# Step 1: Delete rows for researchers with only one match flagged as an outlier
filtered_results['remaining_matches'] = filtered_results[['match1', 'match2', 'match3']].notna().sum(axis=1)
filtered_results = filtered_results[
    ~filtered_results.apply(
        lambda row: row['remaining_matches'] == 1 and f"match{row['remaining_matches']}" in outlier_dict.get(row['researcher_id'], []),
        axis=1
    )
].copy()


# Step 2: Process records with multiple matches
modified_researchers = []

# Updated process_row function
def process_row(row):
    researcher_id = row['researcher_id']
    if researcher_id in outlier_dict:
        # Get matches flagged as outliers
        flagged_matches = outlier_dict[researcher_id]
        was_modified = False

        # Remove flagged matches
        for match in flagged_matches:
            if row[match] is not None:
                row[match] = None
                was_modified = True

        # If any match was removed, clear dependent columns for recalculation
        if was_modified:
            row['ids'] = None
            row['number_ids'] = None
            row['max_date'] = None
            row['min_date'] = None
            row['max_date_interval'] = None
            row['max_min_interval'] = None
            modified_researchers.append(researcher_id)

    return row

filtered_results = filtered_results.apply(process_row, axis=1)

def recalculate_researcher(row):
    remaining_matches = [row['match1'], row['match2'], row['match3']]
    remaining_matches = [match for match in remaining_matches if pd.notna(match)]

    if not remaining_matches:
        return row

    # Find papers authored by the remaining matches
    matched_ids = []
    for match in remaining_matches:
        papers = df1_clean[
            (df1_clean[author_columns].apply(lambda x: match in x.values, axis=1))
        ]['id'].tolist()
        matched_ids.extend(papers)

    # Ensure unique paper IDs
    matched_ids = list(set(matched_ids))

    if matched_ids:
        paper_dates = df1_clean[df1_clean['id'].isin(matched_ids)]['date']
        max_date = paper_dates.max()
        min_date = paper_dates.min()
        max_min_interval = (max_date - min_date).days / year_days
        max_date_interval = (max_dateAPS - max_date).days / year_days

        # Update the row with recalculated values
        row['ids'] = ', '.join(matched_ids)
        row['number_ids'] = len(matched_ids)
        row['max_date'] = max_date.strftime('%Y-%m-%d')
        row['min_date'] = min_date.strftime('%Y-%m-%d')
        row['max_date_interval'] = round(max_date_interval, 1)
        row['max_min_interval'] = round(max_min_interval, 1)

    return row

# Apply recalculation only to modified researchers
filtered_results.loc[
    filtered_results['researcher_id'].isin(modified_researchers)
] = filtered_results.loc[
    filtered_results['researcher_id'].isin(modified_researchers)
].apply(recalculate_researcher, axis=1)

# Save intermediate results after update (optional)
filtered_results.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc_filtered.csv', sep=';', index=False) # Change