# -*- coding: utf-8 -*-
'''
to calculate the expected price change dp_j based on a given x, where
x is the vector of current empirical prices, ending in our current price

equation:
dpj = (sum over i=1 to n(y_i * exp(c(x,x_i))))/(sum over i=1 to n(exp(c(x,x_i)))
n = 20 for our given set of patterns
x_i is a given pattern
y_i is the price change for the kmeans pattern
c is a constant chosen for best fit
defined in the paper
'''

import math
import numpy as np

def bayesian(x, S):
    # based on the length of x, we choose S_j
    dpj = 0

    c = -1/4 # TODO choose a better c, should it be negative or not??
    # compare x with the it in S using our similarity measure
    # and return the conditional expectation, which is dp
    num = 0.0
    den = 0.0

    for i in range(20):
        cutS = S[i, (1:len(x))]
        distance = math.exp(c * (np.linalg.norm(x - cutS, 2) ** 2))
        num = num + S[i, len(x)+1] * distance
        den = den + distance


    if den != 0:
        dpj = num/den
    
    return dpj