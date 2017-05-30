#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:10:45 2016

@author: kristin dahl
"""

import math

# Dependence and Independence: We say that two events are independent if the 
# probability that they both happen is the product of theprobabilities of each 
# one. P(E,F) = P(E)P(F)

# Conditional Probability: the probability of E "conditional on F": 
# P(E|F) = P(E,F)/P(F)  or rewirtten as P(E,F) = P(E|F)P(F) = P(E)

# Bayes's Theorem: A way of "reversing" conditional probabilities. 
# Stated: P(E|F) = P(F|E)P(E)/[P(F|E)P(E) + P(F|!E)P(!E)]


# Random Variables - variable whose possible values have an associated 
# probability distribution. The expected value of a random variable is the 
# average of its values weighted by their probabilities.

# Discrete vs. Continuous Distributions. 

# Probability Density Function: Represents a continuous distribution such that 
# the prbability of seeing a value in a certain interval equals the integral of 
# the density function over the interval.
def uniform_pdf(x):
    return 1 if x >= 0 and x < 1 else 0

# Cumulative Distribution Function: Gives the probability that a random 
# variable is less than or equal to a certain value.
def uniform_cdf(x):
    "returns the probability that a uniform random variable is <= x"
    if x < 0: return 0      # uniform random is never less than 0
    elif x < 1: return x    # e.g. P(X <= 0.4) = 0.4
    else:       return 1    # uniform rando is always less than 1
    
# The Normal Distribution: Classic bell-curve, determined by its mean (mu) and 
# standard deviation (sigma).
def normal_pdf(x, mu=0, sigma=1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-(x-mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))

# Cumulative distriution function for the normal distribution
def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find approximate inverse using binary search"""
    
    # if not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)
        
    low_z, low_p = -10.0, 0      # normal_cdf(-10) is (very close to) 0
    hi_z, hi_p   =  10.0, 0      # normal_cdf(10) is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2    # Consider the midpoint
        mid_p = normal_cdf(mid_z)     # and the cdf's value there
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint is still too high, search below it
            hi_z, hi_p = mid_z, mid_p
        else: 
            break
        
# The Cenral Limit Theorem: A random variable defined as the average of a 
# large number of independent and identically distributed random variables 
# is itself approximately normally distributed.

def bernoulli_trial(p):
    return 1 if random.random() < p else 0

def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))






