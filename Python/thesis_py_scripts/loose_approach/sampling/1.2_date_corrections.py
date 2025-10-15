import pandas as pd

max_date_aps = pd.to_datetime('2021-12-30')
loose_name_results = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc_filtered.csv', sep=';')

loose_name_results['max_date'] = pd.to_datetime(loose_name_results['max_date'])
loose_name_results['min_date'] = pd.to_datetime(loose_name_results['min_date'])

loose_name_results.drop(columns={'max_date_interval', 'max_min_interval'}, inplace = True)

loose_name_results['max_date_interval'] = round((max_date_aps - loose_name_results['max_date']).dt.days / 365.242, 1)
loose_name_results['max_min_interval'] = round((loose_name_results['max_date'] - loose_name_results['min_date'] ).dt.days / 365.242, 1)

# Save filtered results to CSV
loose_name_results.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_results_96prc_filtered.csv',sep=';',index=False)