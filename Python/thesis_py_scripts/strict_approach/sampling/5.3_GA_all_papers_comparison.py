import os
import pandas as pd

# Paths to unique CSV and the directory with 50 CSV files
unique_csv_path = "/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers.csv" # Change
files_directory = "/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_subsets_GA/all_papers" # Change

# Load the unique CSV file
unique_df = pd.read_csv(unique_csv_path, sep=';')

# Extract max_date_interval and max_min_interval from unique CSV
unique_max_date_interval = unique_df["max_date_interval"].mean()
unique_max_min_interval = unique_df["max_min_interval"].mean()

# List to store file details with their differences
differences = []

# Iterate through each CSV file in the directory
for file_name in os.listdir(files_directory):
    if file_name.endswith(".csv"):
        file_path = os.path.join(files_directory, file_name)
        
        # Load the current CSV file
        df = pd.read_csv(file_path, sep=';')
        
        # Calculate the average of max_date_interval and max_min_interval
        avg_max_date_interval = df["max_date_interval"].mean()
        avg_max_min_interval = df["max_min_interval"].mean()
        
        # Compute absolute differences
        diff_max_date_interval = abs(avg_max_date_interval - unique_max_date_interval)
        diff_max_min_interval = abs(avg_max_min_interval - unique_max_min_interval)
        
        # Store the differences, averages, and file name
        differences.append({
            "file_name": file_name,
            "diff_max_date_interval": diff_max_date_interval,
            "diff_max_min_interval": diff_max_min_interval,
            "avg_max_date_interval": avg_max_date_interval,
            "avg_max_min_interval": avg_max_min_interval
        })

# Sort files by "diff_max_min_interval" first, then by "diff_max_date_interval"
sorted_files = sorted(differences, key=lambda x: (x["diff_max_min_interval"], x["diff_max_date_interval"]))[:5]

# Print the top 5 files
print("Top 5 files with smallest differences:")

print(f"Target career:{unique_max_min_interval:.5f} // Target Max Date interval {unique_max_date_interval:.5f}")
for file in sorted_files:
    print(f"File: {file['file_name']}, Diff career: {file['diff_max_min_interval']:.5f}, Diff Max Date Interval: {file['diff_max_date_interval']:.5f}, Avg career: {file['avg_max_min_interval']:.5f}, Avg Max Date Interval: {file['avg_max_date_interval']:.5f}")

# List to store consolidated metrics # New addition
consolidated_results = []

# Function to compute metrics for a given DataFrame
def compute_metrics_lgbt(df, label):
    metrics = {
        "label": label,
        "number_ids_sum": df["number_ids"].sum(),
        "number_ids_avg": round(df["number_ids"].mean(),2),
        "sum_cc_sum": int(df["sum_cc"].sum()),
        "sum_cc_avg": round(df["sum_cc"].mean(),2),
        "sum_PagRank_score_inf": df["sum_PagRank_score_inf"].sum(),
        "sum_AttRank_score_pop": df["sum_AttRank_score_pop"].sum(),
        "sum_3year_cc_imp": int(df["sum_3year_cc_imp"].sum()),
        "avg_max_date_interval": round(df["max_date_interval"].mean(),2),
        "avg_max_min_interval": round(df["max_min_interval"].mean(),2)
    }
    return metrics

def compute_metrics(df, label):
    metrics = {
        "label": label,
        "number_ids_sum": df["number_ids"].sum(),
        "number_ids_avg": round(df["number_ids"].mean(),2),
        "sum_cc_sum": int(df["sum_cc"].sum()),
        "sum_cc_avg": round(df["sum_cc"].mean(),2),
        "sum_PagRank_score_inf": df["sum_pagerank_inf"].sum(),
        "sum_AttRank_score_pop": df["sum_attrank_pop"].sum(),
        "sum_3year_cc_imp": int(df["sum_3year_cc_imp"].sum()),
        "avg_max_date_interval": round(df["max_date_interval"].mean(),2),
        "avg_max_min_interval": round(df["max_min_interval"].mean(),2)
    }
    return metrics

# Compute metrics for the unique CSV
consolidated_results.append(compute_metrics_lgbt(unique_df, "unique_strict_researchers_all_papers"))

# Compute metrics for the top 5 recommended files
for file in sorted_files:
    file_path = os.path.join(files_directory, file["file_name"])
    df = pd.read_csv(file_path, sep=';')
    consolidated_results.append(compute_metrics(df, file["file_name"]))

# Create a DataFrame for consolidated results
consolidated_df = pd.DataFrame(consolidated_results)

# Save the consolidated results to a new CSV file
output_path = "/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_subsets/GA_consol_metrics_all_papers.csv" # Change
consolidated_df.to_csv(output_path, sep= ';', index=False)

print(f"Consolidated metrics saved to {output_path}")