import pandas as pd
import numpy as np
import os
import time
import datetime

# Load data APS Dataset not included on LGBT researchers/authors matches
filtered_candidates = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/filtered_candidates.csv', sep=';') # Change
filtered_candidates = filtered_candidates.rename(columns={"author_name": "input_value"})

filtered_candidates_metadata = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/filtered_candidates_metadata.csv', sep=';') # Change
filtered_candidates_metadata = filtered_candidates_metadata.rename(columns={"input_value": "author_name"})

# Load data of LGBT researchers/authors matches
unique_strict_researchers_nonE = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/unique_strict_researchers_nonC5.csv', sep=';') # Change

len_filtered = len(filtered_candidates)
# Target averages from LGBTQ dataset
target_avg_max_date_interval = unique_strict_researchers_nonE['max_date_interval'].mean()
target_avg_max_min_interval = unique_strict_researchers_nonE['max_min_interval'].mean()
print(f"targets// from last date of APS: {target_avg_max_date_interval} // career:{target_avg_max_min_interval}")

# Exclude APS researchers/authors with older final paper IDs
filtered_candidates = filtered_candidates[filtered_candidates['max_date_interval'] <= unique_strict_researchers_nonE['max_date_interval'].max()]

len_filtered_after_excluding_values_with_greater_max_date_interval_than_max_of_LGBTQ = len(filtered_candidates)
print(f"Pre-filtered candidates: {len_filtered_after_excluding_values_with_greater_max_date_interval_than_max_of_LGBTQ} remaining from {len_filtered} original rows.")

# Parameters
num_samples = 5
iterations = 10
used_authors = set()

output_dir = '/data2/aris/metadata/aps-dataset-metadata-2021/strict_appr/strict_subsets/papers_nonE/' # Change
os.makedirs(output_dir, exist_ok=True)


# Start processing
total_start_time = time.time()  # Start time for the whole process
ct = datetime.datetime.now() # Current time
print(f"Starting subset generation...at {ct}")

for it in range(iterations):
    # Sample authors randomly, seed the random generator with the current time
    np.random.seed(int(time.time()))

    # Set tolerance for matching averages
    tolerance_max_date = 1.0 # changed
    tolerance_max_min = 1.5 # changed

    sub_found_count = 0 # Added to track success/failure
    sub_failed_count = 0

    for i in range(num_samples):
        subset_start_time = time.time()  # Start time for this subset

        # Filter remaining authors who haven't been used
        remaining_authors = filtered_candidates[~filtered_candidates['input_value'].isin(used_authors)].copy() # Added .copy to avoid warning

        # Initialize an empty subset
        valid_subset = pd.DataFrame()
        subset_found = False

        # Calculate weights for sampling based on proximity to the target averages
        remaining_authors.loc[:,'weight'] = (
            1 / (
                abs(remaining_authors['max_date_interval'] - target_avg_max_date_interval) +
                abs(remaining_authors['max_min_interval'] - target_avg_max_min_interval) + 1e-6  # Small constant to avoid division by zero
            )
        )

        # Normalize weights to sum to 1
        remaining_authors.loc[:,'weight'] /= remaining_authors['weight'].sum()

        # Iteratively sample subsets to match target averages
        for attempt in range(10000):  # Limit attempts to avoid infinite loops

            try:
                sampled_authors = remaining_authors.sample(
                    n=len(unique_strict_researchers_nonE),  # Change
                    weights=remaining_authors['weight'],  # Use weights for sampling
                    random_state=np.random.randint(0, 1000000)
                )
            except ValueError:
                print(f"Not enough authors remaining for sample {i + 1}.")
                break
            
            # Calculate averages for the sampled subset
            avg_max_date_interval = sampled_authors['max_date_interval'].mean()
            avg_max_min_interval = sampled_authors['max_min_interval'].mean()

            # Check if the sampled subset meets the tolerance range     # added/changed percentages if needed
            if (abs(avg_max_date_interval - target_avg_max_date_interval) <= tolerance_max_date and
                    abs(avg_max_min_interval - target_avg_max_min_interval) <= tolerance_max_min):
                valid_subset = sampled_authors
                subset_found = True
                sub_found_count += 1
                break

            if attempt % 2000 == 0 and attempt > 0:
                tolerance_max_date *= 1.1
                tolerance_max_min *= 1.04
                print(f"New tolerance for Iteration: {it + 1}, Subset: {i + 1} on date from Last APS data: {round(tolerance_max_date,5)}, career: {round(tolerance_max_min,5)}")

        if not subset_found:
            print(f"Failed to generate a valid subset for sample {i + 1} within tolerance.")
            sub_failed_count += 1
            continue

        # Drop duplicates and merge with metadata
        valid_subset = pd.merge(valid_subset, filtered_candidates_metadata, left_on='input_value', right_on='author_name', how='left')
        valid_subset.drop(columns='author_name', inplace=True)

        # Update the used authors set
        used_authors.update(valid_subset['input_value'])

        # Save the valid subset to a CSV file
        output_file_path = os.path.join(output_dir, f'Iter_{it + 1}_APS_subset_{i + 1}_nonC5.csv')
        valid_subset.to_csv(output_file_path, sep=';', index=False)

        # Calculate and print progress and time taken
        subset_end_time = time.time()
        elapsed_time = subset_end_time - subset_start_time
        print(f"Subset {i + 1}/{num_samples} generated for iteration {it + 1}! Time taken for this subset: {elapsed_time:.2f} seconds. Progress: {sub_found_count}/{num_samples} Completed, {sub_failed_count}/{num_samples} Failed.")

# End of the whole process
total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time
print(f"Process Completed! Total time taken: {total_elapsed_time:.2f} seconds, or {(total_elapsed_time/60):.2f} minutes.")