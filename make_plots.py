# -*- coding: utf-8 -*-
'''
make plots and print out useful stats
'''

import numpy as np
import matplotlib.pyplot as plt

def make_plots(prices, buy, sell, proba, bank, error):

	n = len(prices)
	sbuy = np.full((n,1), np.nan)
	ssell = np.full((n,2), np.nan)
	sbuy[buy] = prices[buy]
	ssell[sell] = prices[sell]

	print('Error of prediction, on average: %d\n', error/n)
	print('Win rate: %d percent\nTotal profit: $%d \n', proba, bank)
	print('Percent profit(approx): %d\n', bank * 100/prices[len(prices)])

	# create plots of buy/sell points
	# note: cannot plot when running on -nojvm flag
	plt.figure(1)
	plt.plot(1:n,prices,'blue')                          # ISSUE: Still need to figure out Matlab to python syntax conversion
	plt.plot(1:n,sbuy,'.red' ,'MarkerSize',20)           # ISSUE: Still need to figure out Matlab to python syntax conversion
	plt.plot(1:n,ssell,'.green' ,'MarkerSize',20)        # ISSUE: Still need to figure out Matlab to python syntax conversion
	plt.show()