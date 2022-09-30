import numpy as np

def mean_squared(x, y):
    return ((x - y) ** 2).sum() / len(y)

def quasi_likelihood(truth=None, predicted=None):
    ratio = truth / predicted
    return (ratio - np.log(ratio) - 1).sum()