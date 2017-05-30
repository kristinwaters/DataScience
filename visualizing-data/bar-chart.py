#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 21:43:12 2016

@author: kristin
"""

from matplotlib import pyplot as plt
from collections import Counter


# Bar Chart - useful when you want to show how a quantity varies among a 
# discrete set of items.

movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
num_oscars = [5, 11, 3, 8, 10]

# Bars are by default width 0.8. So, add 0.1 to the left coordinates so that 
# each bar is centered
xs = [i + 0.1 for i, _ in enumerate(movies)]
      
# Plot bars with left x-coordinates [xs], heights [num_oscars]
plt.bar(xs, num_oscars)

plt.ylabel("# of Academy Awards")
plt.title("My Favorite Movies")

# Label x-axis with movie names at bar centers
plt.xticks([i + 0.5 for i, _ in enumerate(movies)], movies)

plt.show()

# Bar charts are also good for plotting histograms in order to show how 
# values are distributed.

grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]
decile = lambda grade: grade // 10 * 10
histogram = Counter(decile(grade) for grade in grades)

plt.bar([x - 4 for x in histogram.keys()], # Shift each bar to the left by 4
         histogram.values(),               # Give each bsr its correct height
         8)                                # Give each bar a width of 8

plt.axis([-5, 105, 0, 5])                  # x-axis from -5 to 105, 
                                           # y-axis from 0 to 5

plt.xticks([10 * i for i in range(11)])    # x-axis laels at 0, 10, ...., 100
plt.xlabel("Decile")
plt.ylabel("# of Students")
plt.title("Distribution of Exam 1 Grades")
plt.show()
         