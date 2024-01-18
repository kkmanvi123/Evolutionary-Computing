"""
Unit tests for the stack data structure
test_methodname.... etc.
"""

import pytest
import ta_sorting as ta
import pandas as pd

# Sample data for testing
sol1 = pd.read_csv('test1.csv', header=None).values
sol2 = pd.read_csv('test2.csv', header=None).values
sol3 = pd.read_csv('test3.csv', header=None).values

# Test for overallocation
def test_overallocation():
    expected_scores = [37, 41, 23]
    for sol, expected in zip([sol1, sol2, sol3], expected_scores):
        assert ta.overallocation(sol) == expected, f'Expected score {expected}'

# Test for conflicts
def test_conflicts():
    expected_scores = [8, 5, 2]
    for sol, expected in zip([sol1, sol2, sol3], expected_scores):
        assert ta.conflicts(sol) == expected, f'Expected score {expected}'

# Test for undersupport
def test_undersupport():
    expected_scores = [1, 0, 7]
    for sol, expected in zip([sol1, sol2, sol3], expected_scores):
        assert ta.undersupport(sol) == expected, f'Expected score {expected}'

# Test for unwilling
def test_unwilling():
    expected_scores = [53, 58, 43]
    for sol, expected in zip([sol1, sol2, sol3], expected_scores):
        assert ta.unwilling(sol) == expected, f'Expected score {expected}'

# Test for unpreferred
def test_unpreferred():
    expected_scores = [15, 19, 10]
    for sol, expected in zip([sol1, sol2, sol3], expected_scores):
        assert ta.unpreferred(sol) == expected, f'Expected score {expected}'

