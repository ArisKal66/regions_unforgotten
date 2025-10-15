import pandas as pd

loose_name_results = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc.csv', sep=';')

filtered_results = loose_name_results[
    (loose_name_results['number_ids'] > 0) |  # Keep rows where number_ids > 0
    (loose_name_results[['match1', 'match2', 'match3']].notna().any(axis=1))  # OR at least one match column is not NaN
]

# Save filtered results to CSV
filtered_results.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc_filtered.csv',sep=';',index=False)