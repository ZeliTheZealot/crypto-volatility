import numpy as np
from scipy.stats import norm

def autocovariance(array, length, lag, array_mean):
    running_sum = 0
    for i in np.arange(lag, length):
          running_sum += (array[i] - array_mean) * (array[i - lag] - array_mean)
    return running_sum / length

def diebold_mariano_variance_estimate(array, forecast_dependency):
    array = np.array(array)
    length = len(array)
    array_mean = array.mean()
    autocovariances = [autocovariance(array, length, lag, array_mean) for lag in range(0, forecast_dependency)]
    variance_estimate = (autocovariances[0] + 2 * sum(autocovariances[1:])) / length
    return variance_estimate

def normalised_stat(mean, variance):
    return mean / np.sqrt(variance)

def normal_p_value(normalised_stat):
    return 2 * norm.cdf(- abs(normalised_stat))