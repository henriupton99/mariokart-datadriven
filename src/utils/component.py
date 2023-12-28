import polars as pl

class ComponentClass:
    def __init__(self, metadata_path, component_col):
        self.component_col = component_col
        self.metadata = (
            pl.read_csv(metadata_path)
            .rename({"WG":"wei","AC":"acc","OF":"trac",
                "SL":"spd","TL":"han","IV":"inv","MT":"mt"}
            )
            .select([component_col,"wei","acc","trac","spd","han"])
        )
        self.items = self.metadata[component_col]
        
    def get_stats(self, query_name):
        return (
            self.metadata
                .filter(pl.col(self.component_col) == query_name)
                .drop(self.component_col)
                .to_numpy()[0]
            )