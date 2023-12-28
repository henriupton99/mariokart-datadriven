from typing import Union
from src.scoring.metrics import WeightedSum

class Scorer:
    """Scoring class : initializes the combination set universe, and allows to get optimum 
    given a metric class function (cf. metrics)
    """
    def __init__(self, combinations_list, weights):
        """Initialization of the class

        Args:
            combinations_list (list[str]): list of strings representing (stats_values):[possibilities]
            (cf. preprocessing part)
            weights (dict[str,float]): dictionnary of weights to compute the metric scores
        """
        self.weights = weights
        
        # Names of the weights in same order than the combination list input:
        names = ["wei","acc","trac","spd","han"]
        # Processing of combinations list :
        self.combinations = []
        for combination in combinations_list:
            stats, possibilities = combination.split(";")
            stats = tuple(map(int,stats.replace("(","").replace(")","").split(",")))
            stats = {names[k]:value for k,value in enumerate(stats)}
            possibilities = possibilities.split(",")
            self.combinations.append({'stats':stats, 'possibilities':possibilities})
            
    def get_optimum(self, metric) -> dict[str,Union[dict[str,float],list[str]]]:
        """Computes the input metric scores for each combination stats of the list
        and returns the optimum combination stats and its associated components combinations

        Args:
            metric (Metric): metric wrt implementation of metric class

        Returns:
            optimal combination items : stats and list of associated combinations
        """
        # Verify that the input metric is in the set of implemented metrics:
        assert metric in [WeightedSum], "Input metric is not valid"
        # Definition of the metric and verification that objective is valid:
        m = metric(self.weights)
        assert m.obj in ["min","max"], "Metric objective must be 'min' or 'max'"
        # Compute scores for each combinations of the list, find the index of the optimum:
        scores = list(map(m,self.combinations))
        idx_opt = scores.index(max(scores)) if m.obj=="max" else scores.index(min(scores))
        return self.combinations[idx_opt]