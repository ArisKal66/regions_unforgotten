import pandas as pd
from rapidfuzz import process, fuzz
import numpy as np
from tqdm import tqdm  # Progress bar for loops
from datetime import datetime

# Start timing
start_time = datetime.now()

max_dateAPS = '2021-12-30'

# Define columns and load data
author_columns = [f'author{i}' for i in range(1, 27)]
dtypes = {'author23': str, 'author24': str, 'author25': str, 'author26': str}

# Load APS dataset
df1_clean = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/df1_clean1.csv', sep=';', dtype=dtypes)

# Preprocess authors and filter last 50 years
min_date = '1971-12-30'
APS_last_50yrs = df1_clean[df1_clean['date'] >= min_date].copy()
APS_last_50yrs[author_columns] = APS_last_50yrs[author_columns].fillna('')

# Remove dots in author names
for col in author_columns:
    APS_last_50yrs[col] = APS_last_50yrs[col].str.replace('.', '', regex=False)

# Get unique candidates
candidates_last_50yrs = np.unique(APS_last_50yrs[author_columns].values.flatten())
candidates_last_50yrs = candidates_last_50yrs[candidates_last_50yrs != '']  # Remove empty strings

# Load df2
df2 = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/lgbtq_researchers.csv', sep = ';')

# Define columns for results
columns = ['researcher_id', 'input_value', 'ids', 'number_ids', 'max_date', 'min_date', 'max_date_interval', 'max_min_interval']

# Function to find best matches and store match1, match2, match3, etc.
def find_best_matches_loose(APS_last_50yrs, candidates_last_50yrs, columns):
    result_data = []

    # Add a progress bar to the loop
    for index, row in tqdm(df2.iterrows(), total=df2.shape[0], desc="Processing researchers"):
        researcher_id = row['researcher_id']
        input_value = row['first_last_name']
        edited_value = row['fl_edited']

        # Gather matches for both input_value and fl_edited
        matched_data = []
        for value in [input_value, edited_value]:
            matches = process.extract(value, candidates_last_50yrs, scorer=fuzz.ratio, limit=10)
            for match, score, _ in matches:
                if score >= 96:
                    ids = APS_last_50yrs[
                        (APS_last_50yrs[author_columns] == match).any(axis=1)
                    ]['id'].values
                    number_ids = len(ids)
                    max_date = APS_last_50yrs[
                        (APS_last_50yrs[author_columns] == match).any(axis=1)
                    ]['date'].max()
                    min_date = APS_last_50yrs[
                        (APS_last_50yrs[author_columns] == match).any(axis=1)
                    ]['date'].min()
                    max_date = pd.to_datetime(max_date)
                    min_date = pd.to_datetime(min_date)
                    max_date_interval = round((pd.to_datetime(max_dateAPS) - max_date).days / 365.242, 1)
                    max_min_interval = round((max_date - min_date).days / 365.242, 1) if max_date and min_date else 0.0

                    matched_data.append({
                        'match': match,
                        'score': score,
                        'ids': ', '.join(ids),
                        'number_ids': number_ids,
                        'max_date': max_date,
                        'min_date': min_date,
                        'max_date_interval': max_date_interval,
                        'max_min_interval': max_min_interval
                    })

        # Sort matched_data by score (descending) and truncate to 3 matches
        matched_data = sorted(matched_data, key=lambda x: x['score'], reverse=True)[:3]

        # Prepare result row
        result_row = {
            'researcher_id': researcher_id,
            'input_value': input_value,
            'ids': ', '.join([match['ids'] for match in matched_data]),
            'number_ids': sum([match['number_ids'] for match in matched_data]),
            'max_date': max([match['max_date'] for match in matched_data], default=pd.NaT),
            'min_date': min([match['min_date'] for match in matched_data], default=pd.NaT),
            'max_date_interval': max([match['max_date_interval'] for match in matched_data], default=0.0),
            'max_min_interval': max([match['max_min_interval'] for match in matched_data], default=0.0)
        }

        # Add match1, match2, match3, and score1, score2, score3 columns
        for i, match in enumerate(matched_data, start=1):
            result_row[f'match{i}'] = match['match']
            result_row[f'score{i}'] = match['score']

        # Fill missing matches/scores with NaN
        for i in range(len(matched_data) + 1, 4):
            result_row[f'match{i}'] = np.nan
            result_row[f'score{i}'] = np.nan

        result_data.append(result_row)

    return pd.DataFrame(result_data, columns=columns + [f'match{i}' for i in range(1, 4)] + [f'score{i}' for i in range(1, 4)])

# Call function and generate results
loose_name_results = find_best_matches_loose(APS_last_50yrs, candidates_last_50yrs, columns)

# Save results to CSV
loose_name_results.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc.csv', sep=';', index=False)

# Print timing
end_time = datetime.now()
print(f"Script completed in: {end_time - start_time}")