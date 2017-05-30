#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 16:48:44 2016

@author: kristin dahl
"""

# Here I will represent matrices as lists of lists

# Consider the shape of the matrix as the number of rows/columns
def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols
    
def get_row(A, i):
    return A[i]

def get_column(A, j):
    return [A_i[j] for A_i in A]

# Also we want to be able to make a matrix given its shape and a function for 
# generating its elements.
def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix
    whose (i,j)th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j) 
             for j in range(num_cols)]
             for i in range(num_rows)]

# Identity Matrix
# identity_matrix = make_matrix(5, 5, is_diagonal)
def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0
    


