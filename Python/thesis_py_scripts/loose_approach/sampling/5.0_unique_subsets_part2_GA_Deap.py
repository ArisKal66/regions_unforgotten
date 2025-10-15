import pandas as pd
import numpy as np
import os
import time
import datetime
from deap import base, creator, tools, algorithms
import random
from tqdm import tqdm

# Load data (same as before)
filtered_candidates = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/filtered_candidates_96prc.csv', sep=';')
filtered_candidates_tb_merged = filtered_candidates[['author_name','number_ids','max_date_nonC5','min_date_nonC5','max_date_interval_nonC5','max_min_interval_nonC5','max_date','min_date','max_date_interval','max_min_interval']]
filtered_candidates = filtered_candidates.rename(columns={"author_name": "input_value"})

filtered_candidates_metadata = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/filtered_candidates_96prc_metadata.csv', sep=';')
filtered_candidates_metadata = filtered_candidates_metadata.rename(columns={"input_value": "author_name"})

unique_strict_researchers_nonE = pd.read_csv('/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/unique_loose96prc_researchers_nonC5.csv', sep=';')

len_filtered = len(filtered_candidates)
target_avg_max_date_interval = unique_strict_researchers_nonE['max_date_interval'].mean()
target_avg_max_min_interval = unique_strict_researchers_nonE['max_min_interval'].mean()
print(f"targets// from last date of APS: {target_avg_max_date_interval} // career:{target_avg_max_min_interval}")

filtered_candidates = filtered_candidates[filtered_candidates['max_date_interval'] <= unique_strict_researchers_nonE['max_date_interval'].max()]

len_filtered_after_excluding_values_with_greater_max_date_interval_than_max_of_LGBTQ = len(filtered_candidates)
print(f"Pre-filtered candidates: {len_filtered_after_excluding_values_with_greater_max_date_interval_than_max_of_LGBTQ} remaining from {len_filtered} original rows.")

# --- Genetic Algorithm Setup ---

# Parameters
num_samples = 5
iterations = 10
subset_size = len(unique_strict_researchers_nonE)  # Target subset size
used_authors = set()

output_dir = '/data2/aris/metadata/aps-dataset-metadata-2021/loose_appr/96prc/loose_subsets_GA/papers_nonE/'
os.makedirs(output_dir, exist_ok=True)

# Fitness function: Evaluate an individual (subset)
def evaluate_subset(individual):
    subset_authors = [filtered_candidates_list[i] for i in individual if i < len(filtered_candidates_list)] # Changed to include individuals that are in the filtered_candidates_list
    subset_df = filtered_candidates[filtered_candidates['input_value'].isin(subset_authors)]

    if len(subset_df) < len(individual):
        return 1e6, 1e6 # Returning a tuple, added this to address cases where no authors are found in filtered_candidates

    avg_max_date_interval = subset_df['max_date_interval'].mean()
    avg_max_min_interval = subset_df['max_min_interval'].mean()

    # Calculate the difference from target averages
    diff_max_date = abs(avg_max_date_interval - target_avg_max_date_interval)
    diff_max_min = abs(avg_max_min_interval - target_avg_max_min_interval)

    # You can add more criteria to the fitness function here if needed
    # e.g., penalize for uneven distribution of career lengths

    return diff_max_date, diff_max_min  # Return a tuple of differences

# --- DEAP Setup ---
filtered_candidates_list = filtered_candidates['input_value'].tolist() # Added to convert filtered candidates to a list

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))  # Minimize both differences
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_item", random.randrange, len(filtered_candidates))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, n=subset_size)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate_subset)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(filtered_candidates) - 1, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# --- Main Loop ---

total_start_time = time.time()
ct = datetime.datetime.now()
print(f"Starting subset generation with Genetic Algorithm...at {ct}")

for it in range(iterations):

    np.random.seed(int(time.time())) # Seed for reproducibility on each iteration

    for i in range(num_samples):
        subset_start_time = time.time()

        # Initialize population
        pop = toolbox.population(n=50)  # Population size: 50

        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # Genetic Algorithm parameters
        CXPB, MUTPB, NGEN = 0.5, 0.2, 50  # Crossover, mutation probabilities, generations # NGEN was 40

        print("  Starting evolutionary process...")
        # Use tqdm for the generation loop
        with tqdm(total=NGEN, desc=f"Subset {i + 1}/{num_samples}, Iter {it + 1}") as pbar:
            for g in range(NGEN):
                # Select the next generation individuals
                offspring = toolbox.select(pop, len(pop))
                # Clone the selected individuals
                offspring = list(map(toolbox.clone, offspring))

                # Apply crossover on the offspring
                for child1, child2 in zip(offspring[::2], offspring[1::2]):
                    if random.random() < CXPB:
                        toolbox.mate(child1, child2)
                        del child1.fitness.values
                        del child2.fitness.values

                # Apply mutation on the offspring
                for mutant in offspring:
                    if random.random() < MUTPB:
                        toolbox.mutate(mutant)
                        del mutant.fitness.values

                # Evaluate the individuals with an invalid fitness
                invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                fitnesses = map(toolbox.evaluate, invalid_ind)
                for ind, fit in zip(invalid_ind, fitnesses):
                    ind.fitness.values = fit

                # Replace population with offspring
                pop[:] = offspring

                # Removed: print(f"      Generation {g + 1} completed.")
                pbar.update(1)  # Update the progress bar

        # Get the best individual (subset)
        best_ind = tools.selBest(pop, 1)[0]
        best_subset_authors = [filtered_candidates_list[idx] for idx in best_ind if idx < len(filtered_candidates_list)] # Changed to include individuals that are in the filtered_candidates_list

        # Create subset dataframe and merge with metadata
        valid_subset = pd.DataFrame({'input_value': best_subset_authors})
        valid_subset = pd.merge(valid_subset, filtered_candidates_metadata, left_on='input_value', right_on='author_name', how='left')
        valid_subset.drop(columns='author_name', inplace=True)
        valid_subset = pd.merge(valid_subset, filtered_candidates_tb_merged, left_on='input_value', right_on='author_name', how='left')
        valid_subset.drop(columns='author_name', inplace=True)
        
        # Update used authors
        used_authors.update(valid_subset['input_value'])

        # Save the valid subset
        output_file_path = os.path.join(output_dir, f'Iter_{it + 1}_APS_subset_{i + 1}_GA_nonC5.csv')
        valid_subset.to_csv(output_file_path, sep=';', index=False)

        subset_end_time = time.time()
        elapsed_time = subset_end_time - subset_start_time
        print(f"Subset {i + 1}/{num_samples} generated for iteration {it + 1} using GA! Time taken: {elapsed_time:.2f} seconds.")

total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time
print(f"Process Completed! Total time taken: {total_elapsed_time:.2f} seconds, or {(total_elapsed_time/60):.2f} minutes.")