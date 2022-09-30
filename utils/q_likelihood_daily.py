import numpy as np
def q_likelihood_daily(y, X, res):
    truth = y[y.index.hour == 0]
    X_daily = X[X.index.hour == 0]
    predicted = np.dot(X_daily, res.params)
    ratio = truth / predicted
    return (ratio - np.log(ratio) - 1).mean()