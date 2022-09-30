import pytest
import sys
import os
sys.path.append(os.getcwd())
from utils.to_be_tested import *

def test_factorial():
    assert fact(4) == 24