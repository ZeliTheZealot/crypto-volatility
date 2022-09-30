import numpy as np

def q_likelihood_oos_details(betas, y, X, window_length):
    sample_length = len(y)
    result = np.zeros(sample_length - window_length)
    for oos_index in range(window_length, sample_length):
        inception_index = oos_index - window_length
        beta = betas.iloc[oos_index]
        y_oos = y.iloc[oos_index]
        X_oos = X.iloc[oos_index]
        predicted = np.dot(X_oos, beta)
        ratio = y_oos / predicted
        q_likelihood = ratio - np.log(ratio) - 1
        result[inception_index] = q_likelihood
    return result