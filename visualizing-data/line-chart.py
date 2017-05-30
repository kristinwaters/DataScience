#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 21:29:13 2016

@author: kristin
"""

from matplotlib import pyplot as plt


# Simple line chart example
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

# Create a line chart, years on x-axis, gdp on y-axis
plt.plot(years, gdp, color='green', marker='o', linestyle='solid')

# Add a title
plt.title("Nominal GDP")

# Add a label to the y-axis
plt.ylabel("Billions of $")
plt.show()

# Line charts are good for showing trends.
variance = [1, 2, 4, 8, 16, 32, 64, 128, 256]
bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]
total_error = [x + y for x, y in zip(variance, bias_squared)]
xs = [i for i, _ in enumerate(variance)]
      
# We can make multiple calls to plt.plot to show multiple series on the same 
# chart.
plt.plot(xs, variance, 'g-', label='variance') # Green solid line
plt.plot(xs, bias_squared, 'r-.', label='bias^2') # Red dot-dashed line
plt.plot(xs, total_error, 'b:', label='total error') # Blue dotted line

# Because we've assigned labels to each series, we can get a legend for free
# loc=9 means "top center"
plt.legend(loc=9)
plt.xlabel("model complexity")
plt.title("The Bias-Variance Tradeoff")
plt.show()