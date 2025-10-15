import pandas as pd

filtered_candidates = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/filtered_candidates_96prc.csv', sep = ';')
filtered_candidates_all_papers = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/filtered_candidates_96prc_all_papers.csv', sep = ';')

filtered_candidates = filtered_candidates.rename(columns={"max_date": "max_date_nonC5","min_date": "min_date_nonC5"})

filtered_candidates_all_papers = filtered_candidates_all_papers.rename(columns={"author_name": "an", "number_ids": "num_ids"})

filtered_candidates = filtered_candidates.merge(filtered_candidates_all_papers, left_on="author_name", right_on="an", how = "left")

filtered_candidates = filtered_candidates.drop(columns=['an', 'num_ids'])
filtered_candidates.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/filtered_candidates_96prc.csv', sep = ';', index= False)