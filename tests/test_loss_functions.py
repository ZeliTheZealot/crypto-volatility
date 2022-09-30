import pytest
import sys
import os
sys.path.append(os.getcwd())

from utils.loss_functions import *
import numpy as np

def test_mean_squared():
    x = np.array([1.5, 3.5])
    y = np.array([0.5, 1.0])
    assert mean_squared(x, y) == 7.25
    
def test_quasi_likelihood():
    truth = np.array([1.5, 3.5])
    predicted = np.array([0.5, 1.0])
    ratio = np.array([3, 3.5])
    log_ratio = np.array([np.log(3), np.log(3.5)])
    assert quasi_likelihood(truth, predicted) == (ratio - log_ratio - 1).sum()
