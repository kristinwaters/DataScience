#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 17:13:45 2016

@author: kristin dahl
"""
from collections import Counter
import math

# We use statistics to distill and communiate relevant features of our data.

# Mean - Sensitive to outliers in data.
def mean(x):
    return sum(x) / len(x)
    
# Median
def median(v):
    """finds the middle-most' value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2
    
    if n %2 == 1:
        # if odd, return the middle value
        return sorted_v[midpoint]
    else:
        # if even, return the average of the middle values
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2

# Quantile - A generalization of the median. Represents the value less than 
# which a certain percentile of the data lies.
def quantile(x, p):
    """returns the pth-percentile value in x"""
    p_index = int(p * len(x))
    return sorted(x)[p_index]

# Mode - most common value[s]
def mode(x):
    """returns a list, might be more than one mode"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.iteritems()
            if count == max_count]


# Dispersion: Refers to measures of how spread out the data is.

# Range - difference between the largest and smallest elements
def data_range(x):
    return max(x) - mi(x)

# Variance - Measures how a single variable deviates from its mean
def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)

# Standard Deviation
def standard_deviation(x):
    return math.sqrt(variance(x))
    
# Interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)


# Correlation

# Covariance - Measures how two variables vary in tandem from their means
def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)
    
# Correlation - Divides out the standard deviations of both variables
def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0 # If no variation, correlation is 0
        


