class WeightedSum:
    """Weighted sum metric : computes simple weighted sum given:
    - combination stats value : {"wei":v1,"acc":v2,"trac":v3,"spd":v4,"han":v5}
    - stats weights : {"wei":w1,"acc":w2,"trac":w3,"spd":w4,"han":w5}
    """
    def __init__(self, weights):
        """Initialization of the class

        Args:
            weights (dict[str,float]): dictionnary of weights for each stats
        """
        # Objective direction : 'max'(resp. 'min') means maximum (resp. minimum) score of the metric is the best
        self.obj = "max"
        self.weights = weights
        
    def __call__(self, combination_stats) -> float:
        """Call of the metric, computation of the score for input combination

        Args:
            combination_stats (dict[str,float]): combination stats values

        Returns:
            (float): score of the metric
        """
        return sum(self.weights[stat] * value for stat,value in combination_stats['stats'].items())