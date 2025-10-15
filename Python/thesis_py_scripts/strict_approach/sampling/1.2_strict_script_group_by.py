import pandas as pd

df = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_fn_results.csv', sep = ';')

def process_matches(group):
    matches = group['match'].tolist()
    scores = group['score'].tolist()
    return pd.Series({
        'match1': matches[0] if len(matches) > 0 else None,
        'match2': matches[1] if len(matches) > 1 else None,
        'score1': scores[0] if len(scores) > 0 else None,
        'score2': scores[1] if len(scores) > 1 else None,
    })

# Group by researcher_id and apply aggregation
grouped_df = (
    df.groupby('researcher_id', as_index=False)
    .agg({
        'input_value': 'first',  # Keep the first input_value (assuming it's the same for all rows of the same researcher_id)
        'ids': lambda x: ', '.join(x),  # Concatenate all IDs
        'number_ids': 'sum',  # Sum the number of IDs
    })
)

# Process matches and scores for the grouped dataframe
matches_scores = df.groupby('researcher_id').apply(process_matches).reset_index()

# Merge the aggregated data with the matches and scores
final_df = pd.merge(grouped_df, matches_scores, on='researcher_id')

final_df.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_fn_results.csv', sep = ';', index = False)