import numpy as np
def mean_squared_oos(betas, y, X, window_length):
    sample_length = len(y) # assume well-behaved
    result = 0
    for oos_index in range(window_length, sample_length): 
        beta = betas.iloc[oos_index] # aligned with oos
        y_oos = y.iloc[oos_index]
        X_oos = X.iloc[oos_index]
        sq_error = (y_oos - np.dot(X_oos, beta)) ** 2
        result += sq_error
    return result / (sample_length - window_length)