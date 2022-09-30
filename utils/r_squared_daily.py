import numpy as np
def r_squared_daily(y, X, res):
    y_daily = y[y.index.hour == 0]
    X_daily = X[X.index.hour == 0]
    beta = res.params
    residual_sum_squares = ((y_daily - np.dot(X_daily, beta)) ** 2).sum()
    centred_sum_squares = ((y_daily - y_daily.mean()) ** 2).sum()
    return 1 - residual_sum_squares / centred_sum_squares