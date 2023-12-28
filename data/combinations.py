import polars as pl
from itertools import product
from tqdm import tqdm

class ComponentClass:
    def __init__(self, metadata_path, component_col):
        self.component_col = component_col
        self.metadata = (
            pl.read_csv(metadata_path)
            .rename({"WG":"wei","AC":"acc","OF":"trac",
                "SL":"spd","TL":"han","IV":"inv","MT":"mt"}
            )
            .select([component_col,"wei","acc","trac","spd","han","inv","mt"])
        )
        self.items = self.metadata[component_col].unique()
        
    def get_stats(self, query_name):
        return (
            self.metadata
                .filter(pl.col(self.component_col) == query_name)
                .drop(self.component_col)
                .to_numpy()[0]
            )
        
components = {
    "Drivers" : ("./metadata/Drivers(DV).txt","Driver"),
    "Tires" : ("./metadata/Tires(TR).txt","Tire"),
    "Bodies" : ("./metadata/Bodies(BD).txt","Body"),
    "Gliders" : ("./metadata/Gliders(WG).txt","Glider")
}
metadatas = {}
for metadata_name, (metadata_path, component_col) in components.items():
    metadatas[metadata_name] = ComponentClass(metadata_path,component_col)

stats_possibilities = {}
for driver,body,tire,glider in tqdm(list(product(
    metadatas["Drivers"].items,
    metadatas["Bodies"].items,
    metadatas["Tires"].items,
    metadatas["Gliders"].items))):
    
    stats = metadatas["Drivers"].get_stats(driver)
    stats += metadatas["Bodies"].get_stats(body)
    stats += metadatas["Tires"].get_stats(tire)
    stats += metadatas["Gliders"].get_stats(glider)
    stats = tuple(stats)
    if stats in stats_possibilities.keys():
        stats_possibilities[stats].append(f"{driver}/{body}/{tire}/{glider}")
    else :
        stats_possibilities[stats] = [f"{driver}/{body}/{tire}/{glider}"]

with open("stats_possibilities.txt","w") as file:
    file.write("stats;combinations\n")
    for stats, combinations in stats_possibilities.items():
        file.write(f"{stats};")
        for i,combination in enumerate(combinations):
            file.write(f"{combination}")
            if i == len(combinations)-1:
                continue
            file.write(",")
        file.write("\n")
    file.close()