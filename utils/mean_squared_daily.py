import numpy as np
def mean_squared_daily(y, X, res):
    y_daily = y[y.index.hour == 0]
    X_daily = X[X.index.hour == 0]
    beta = res.params
    return ((y_daily - np.dot(X_daily, beta)) ** 2).mean()