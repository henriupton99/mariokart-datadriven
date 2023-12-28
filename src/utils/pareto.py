import numpy as np

def pareto_optimal_points(points:np.ndarray) -> np.ndarray:
    """Function that computes identifies the subset of Pareto optimal vectors 
    in a 2D array (first dimension=observations, second dimension=vector components)

    Args:
        points (np.ndarray): array of points observations that describes the universe

    Returns:
        np.ndarray: subset Pareto optimal points of points input array
    """
    # Initialize an "undominated" list full of "True" to update 
    undominated = np.ones(points.shape[0],dtype=bool)
    # Sort points in decreasing order of sum of vector coordinates
    # NB : x=(x1,...,xN) can Pareto dominate y=(y1,...,yN) iif sum(x1,...,xN)>sum(y1,...,yN)
    points = points[points.sum(1).argsort()[::-1]]
    
    # Loop accross all points in the input array :
    for i in range(points.shape[0]):
        n = points.shape[0]
        if i>=n:
            break
        # As the array is sorted, we evaluate the points that goes after points[i] (ie lower sum) 
        # if at least one coordinate of the point is greater than points[i] it means that points[i]
        # doesnt Pareto dominates him, so it stays undominated
        undominated[i+1:n] = (points[i+1:]>=points[i]).any(1)
        # keep only undominated points for computational speed:
        points = points[undominated[:n]]
    return points