# -*- coding: utf-8 -*-
"""
Algo Trading main script

"""
import os
import csv
import numba
import numpy as np
import random
import scipy.io as sio
from sklearn.cluster import KMeans
from scipy.stats.mstats import zscore

import bayesian
import make_plots
import ys_sampEntropy

os.remove('reg.mat') # won't exist on first run

# import prices as column vectors from the csv sheet
# about 120 000 values
dataArray = np.genfromtxt('okcoin5s.csv', delimiter = ',')  # ISSUE: Don't know what the delimiting of this particular file okcoin5s.csv is
prices = dataArray[:, 1]
askVolume = dataArray[:, 2]
bidVolume = dataArray[:, 3]
del dataArray

prices = np.transpose(prices)
# breakpoint for selecting price series
# prices1 = [:b] prices2 = [b:b*2] prices3 = [b*2:]
b = 20000

prices = prices[::2]  #turns 5s to 10s steps
askVolume = askVolume[::2]
bidVolume = bidVolume[::2]

askVolume = askVolume[b+1:len(askVolume)]    # ISSUE: Since this is going to be in python and not Matlab, shouldn't it be "b" instead of "b+1"?
bidVolume = bidVolume[b+1:len(bidVolume)]    # ISSUE: Since this is going to be in python and not Matlab, shouldn't it be "b" instead of "b+1"?

prices1 = prices[0:b]
prices2 = prices[b:b*2]                      # ISSUE: Shouldn't it be "b" instead of "b+1"?
prices3 = prices[b*2:len(prices)]            # ISSUE: Shouldn't it be "b" instead of "b+1"?
'''
Step 1: creating intervals S_j
Create list of all 720*10s, 360*10s and 180*10s intervals each 
item is (interval of prices, NEXT TEN SEC interval price change)
'''

intJump = 1  # idea: separate consecutive intervals from each other slightly 
priceDiff = np.diff(prices)
del prices
validIntSize = len(prices1) - 750; #valid interval size
interval720s = np.zeros((validIntSize, 720))        # CHANGE: Eliminated the +1 due to this being python
interval360s = np.zeros((validIntSize, 360))        # CHANGE: Eliminated the +1 due to this being python
interval180s = np.zeros((validIntSize, 180))        # CHANGE: Eliminated the +1 due to this being python

for i in range(0, validIntSize, intJump):              # CHANGE: Changed the 1 to 0 due to this being python and index being 0
    interval180s[i,:] = [prices1[i:i+179],priceDiff[i+179]]
    interval360s[i,:] = [prices1[i:i+359],priceDiff[i+359]]
    interval720s[i,:] = [prices1[i:i+719],priceDiff[i+719]]

del prices1
del priceDiff
# now we k-means cluster all 3 interval lists to get the 20 best patterns
# for each of the interval lists 

clusters = 100;
# parpool 
# if it doesn't work for you, 
# uncomment the two lines and change UseParallel option to 0
#-------------------------------------------------Current Progress of Python Conversion-----------------------------------------------------------

pool = parpool                      # Invokes workers
random_stream = numpy.random.RandomState()  # Random number stream #ISSUE: This one would hopefully work with numpy.rand(), but 'mlfg6331_64'?
options = statset('UseParallel', 1, 'UseSubstreams', 1, 'Streams', stream)
print('starting clustering')
tic
[ID180, kmeans180s1] = KMeans(interval180s, clusters, 'Options',options, 'MaxIter', 10000, 'Display', 'final', 'Replicates', 4)
[ID360, kmeans360s1] = KMeans(interval360s, clusters, 'Options',options, 'MaxIter', 10000, 'Display', 'final', 'Replicates', 4)
[ID720, kmeans720s1] = KMeans(interval720s, clusters, 'Options',options, 'MaxIter', 10000, 'Display', 'final', 'Replicates', 4)
toc
# consideration: for speed: use similarity instead of L2 norm for kmeans?
del pool

del interval180s
del interval360s
del interval720s
'''
regularize so the mean = 0 and std =1
don't regularize the price jump (at the last index)
'''
for i in range(1, clusters):
	kmeans180s1[i, 1:180] = zscore(kmeans180s1[i, 1:180])
	kmeans360s1[i, 1:360] = zscore(kmeans360s1[i, 1:360])
	kmeans720s1[i, 1:720] = zscore(kmeans720s1[i, 1:720])
end

# use sample entropy to choose interesting/effective patterns 
entropy180 = np.zeros(clusters, 1)
entropy360 = np.zeros(clusters, 1)
entropy720 = np.zeros(clusters, 1)
for i in 1:clusters:
	entropy180[i] = ys_sampEntropy(kmeans180s1[i, 1:180]);
	entropy360[i] = ys_sampEntropy(kmeans360s1[i, 1:180]);   
	entropy720[i] = ys_sampEntropy(kmeans720s1[i, 1:180]); 
	# TODO indexing 1:180 for all three is wrong, but gets 3.8% profits and indexing properly gets less...??
end
# sort by 20 most interesting, and save these
# first pattern for 360s  is the flat pattern/ all 0s

[~,IX] = sorted(entropy180, reverse=True)
IX180 = IX(1:20)
[~,IX] = sorted(entropy360, reverse=True)
IX360 = IX(1:20)
[~,IX] = sorted(entropy720, reverse=True)
IX720 = IX(1:20)
kmeans180s = kmeans180s1[IX180,:]
kmeans360s = kmeans360s1[IX360,:]
kmeans720s = kmeans720s1[IX720,:]

print('finished clustering and normalizing')
del kmeans180s1
# del kmeans360s1
del kmeans720s1

'''
Step 2: predicting average price change dp_j and learning parameters w_i
using Bayesian regression

equation: dp = w0 + w1*dp1 + w2*dp2 + w3*dp3 + w4*r
'''
numFeatures = 3
start = 730
numPoints = len(prices2) - start
regressorX = np.zeros(numPoints, numFeatures)
regressorY = np.zeros(1, numPoints)
for i in range(start, (len(prices2)-1)):
    price180 = zscore(prices2(i-179:i))
    price360 = zscore(prices2(i-359:i))
    price720 = zscore(prices2(i-719:i))
    assert(isequal(len(price180), 180))
    assert(isequal(len(price360), 360))
    assert(isequal(len(price720), 720))
    
    # average price change dp_j is given by bayesian regression    
    dp1 = bayesian(price180, kmeans180s)
    dp2 = bayesian(price360, kmeans360s) 
    dp3 = bayesian(price720, kmeans720s)
    
	# not using r currently
    # to use r: uncomment in these two lines, and edit brtrade.py 
    # r = (bidVolume(i)-askVolume(i))/(bidVolume(i)+askVolume(i)); 
    
	# create data for regression method
    regressorX((i - start + 1), :) = [dp1, dp2, dp3] #,r]
    regressorY(i - start + 1) = prices2[i + 1] - prices2[i]

end

del prices2

# Set up differential evolution optimization
save('reg.mat','regressorX','regressorY')

os.system('Rundeopt.py')

# retrieve weights 
theta = np.zeros(numFeatures, 1)
for k in range(1:numFeatures):
  theta[k] = FVr_x[k]

theta0 = FVr_x[k+1]

# need this to test
save('thetas.mat', 'theta','theta0','kmeans180s','kmeans360s','kmeans720s')

# Start trading with last list of prices
print('Finished regression, ready to trade')
[error, jinzhi, bank, buy, sell, proba] = brtrade(prices3, bidVolume(b+1:end), askVolume(b+1:end), 1)

# set up plots
make_plots(prices3, buy, sell, proba, bank, error)