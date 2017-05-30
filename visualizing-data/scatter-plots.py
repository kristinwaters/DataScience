#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 08:31:58 2016

@author: kristin
"""

from matplotlib import pyplot as plt
from collections import Counter

# Scatterplots let you visualize the relationship between two paired sets of 
# data.

friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels  = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

plt.scatter(friends, minutes)

# Label each point
for label, friend_count, minute_count in zip (labels, minutes, friends):
    plt.annotate(label,
                 xy=(friend_count, minute_count), # put the label with its point
                 xytext=(5, -5),                  # ut slightly offset
                 textcoords='offset points')
    
plt.title("Daily Minutes vs. Number of Friends")