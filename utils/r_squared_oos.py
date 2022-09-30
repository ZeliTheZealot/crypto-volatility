import numpy as np
def r_squared_oos(betas, y, X, window_length):
    sample_length = len(y)
    predictions = np.zeros(sample_length - window_length)
    truths = np.zeros(sample_length - window_length)
    for oos_index in range(window_length, sample_length):
        inception_index = oos_index - window_length
        beta = betas.iloc[oos_index]
        truth = y.iloc[oos_index]
        X_oos = X.iloc[oos_index]
        prediction = np.dot(X_oos, beta)
        predictions[inception_index] = prediction
        truths[inception_index] = truth
    sum_of_squared_differences = ((truths - predictions) ** 2).sum()
    mean_of_truths = truths.mean()
    centered_sum_of_squares = ((truths - mean_of_truths) ** 2).sum()
    return 1 - sum_of_squared_differences / centered_sum_of_squares