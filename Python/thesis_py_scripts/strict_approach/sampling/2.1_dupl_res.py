import pandas as pd

unique_strict = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers.csv', sep = ';')
unique_strict= unique_strict.drop_duplicates()
unique_strict.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers.csv', sep = ';', index = False)

unique_strict_nonC5 = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers_nonC5.csv', sep = ';')
unique_strict_nonC5= unique_strict_nonC5.drop_duplicates()
unique_strict_nonC5.to_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers_nonC5.csv', sep = ';', index = False)