"""Script for creation of the combinations.txt file that represent the set of all possible stats vectors:
Each line represent a possible stats vector ("wei","acc","trac","spd","han")
followed by the list of all combinations of driver/body/tire/glider (d,b,t,g) that can produce this vector :
Example :
- (8, 13, 16, 8, 13);Lakitu/Cat Cruiser/Hot Monster/Flower Glider,Lakitu/Cat Cruiser/Hot Monster/Cloud Glider,Lakitu/Comet/Hot Monster/Flower Glider,Lakitu/Comet/Hot Monster/Cloud Glider)

NB : This script only keeps statistics vectors that are Pareto efficient.
"""

import sys, os
sys.path.insert(0,"..")
import numpy as np
from itertools import product
from tqdm import tqdm

from config import CONFIG
from utils.component import ComponentClass
from utils.pareto import pareto_optimal_points
        
# Load metadata thanks to class ComponentClass :
metadatas = {}
for metadata_name, (metadata_path, component_col) in CONFIG.COMPONENTS.items():
    metadatas[metadata_name] = ComponentClass(metadata_path,component_col)
    
# Create result dictionnary of {stats vector : [combinations for this vector]}
stats_possibilities = {}
# Loop accross all possible combinations of (driver/body/tires/gliders):
combinations = list(product(metadatas["Drivers"].items,metadatas["Bodies"].items,
    metadatas["Tires"].items,metadatas["Gliders"].items))

print(f"Number of possible combinations : {len(combinations)}")
for driver,body,tire,glider in tqdm(combinations):
    
    # Final stats vector is the sum of the levels for each component :
    stats = metadatas["Drivers"].get_stats(driver)
    stats += metadatas["Bodies"].get_stats(body)
    stats += metadatas["Tires"].get_stats(tire)
    stats += metadatas["Gliders"].get_stats(glider)
    stats = tuple(stats)
    
    # If the stats vector already exists in the dictionnary,
    # add the combination (driver/body/tires/gliders) to the key stats :
    if stats in stats_possibilities.keys():
        stats_possibilities[stats].append(f"{driver}/{body}/{tire}/{glider}")
    # Otherwise create a new key stats with combination (driver/body/tires/gliders)
    # as first item of the list :
    else :
        stats_possibilities[stats] = [f"{driver}/{body}/{tire}/{glider}"]

# Computation of the set of Pareto optimal stats vectors :
stats_vectors = np.array([list(stat) for stat in stats_possibilities.keys()])
pareto_optimal_stats = list(map(tuple, pareto_optimal_points(stats_vectors).tolist()))

# We only keep as final dictionnary the Pareto optimal stats vectors :
print("Pareto optimal stats vectors filtering:")
print(f"Before filtering : {len(stats_possibilities)} unique observations")
pareto_optimal_set = {stat : combinations for stat,combinations in stats_possibilities.items()
                      if stat in pareto_optimal_stats}
print(f"After filtering : {len(pareto_optimal_set)} unique observations")

# Write the final result in a text file :
with open(os.path.join(CONFIG.DATA_PATH,"combinations.txt"),"w") as file:
    for stats, combinations in stats_possibilities.items():
        file.write(f"{stats};")
        for i,combination in enumerate(combinations):
            file.write(f"{combination}")
            if i == len(combinations)-1:
                continue
            file.write(",")
        file.write("\n")
    file.close()