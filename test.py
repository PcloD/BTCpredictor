# -*- coding: utf-8 -*-
'''
Testing on August 2017 price data
'''

import csv
import numpy as np

dataArray = csv.csvread('results.csv')
prices = np.transpose(dataArray[:, 2])
askVolume = dataArray[:, 3]
bidVolume = dataArray[:, 4]

prices = prices[1:2:len(prices)]
askVolume = askVolume[1:2:end]
bidVolume = bidVolume[1:2:end]

# estimate transaction fee at %1
[error, jinzhi, bank, buy, sell, proba] = brtrade(prices, bidVolume, askVolume, 1)

# set up plots
make_plots(prices, buy, sell, proba, bank, error)