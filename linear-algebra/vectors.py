#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 16:08:34 2016

@author: kristin dahl
"""
import math

# Vectors are points in some finite-dimensional space.
# Simplest approach: Represent vectors as a list of numbers.

# Note that Python lists are not vectors so we need to build the 
# arithmetic tools from scratch.

# Vector Addition
def vector_add(v, w):
    """adds corresponding elements"""
    return [v_i + w_i for v_i, w_i in zip(v,w)]

# Vector Subtract
def vector_subtract(v, w):
    """subtracts corresponding elements"""
    return [v_i - w_i for v_i, w_i in zip(v,w)]
            
# Component-wise sum a list of vectors
def vector_sum(vectors):
    """sums all corresponding elements"""
    return reduce(vector_add, vectors)

# Scalar Multiply
def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]

# Now we can compute the componentwise means of a list of (same-sized) vectors.
def vector_mean(vectors):
    """compute the vector whose ith element is the mean of the ith elements of 
    the input vectors"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))
    
# The dot product of two vectors is the sum of their componentwise products.
# It measures how far the vector v extends in the w direction.
def dog(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v,w))
    

# You can use the dot product to compute a vector's sum of squares
def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)

# Which we can use to compute the vector magnitude (length)
def magnitude(v):
    return math.sqrt(sum_of_squares(v))

# We can now compute the distance between two vectors
def squared_distance(v, w):
    """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_subtract(v, w))
    
def distance(v, w):
    return magnitude(vector_subtract(v, w))
    
    

