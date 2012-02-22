"""Routines to normalize 1d and 2d array-like objects. """
import numpy as np

def zscore(arr):
	arr = np.array(arr)
	c_std = arr.std(0)
	c_std[c_std == 0.0] = 1.0
		## Replace 0 stdev cols with 1.
	
	return (arr - arr.mean(0)) / c_std
	
def percent_change(arr):
	# x is original, y is transformed,
	# u is the column mean
	# repeat for each row (i) and column (j):
	# 	y_i_j = 100 + ((x_i_j - u_j)/u_j) * 100
	c_mean = arr.mean(0)
	return np.nan_to_num(100 + (((arr-c_mean)/c_mean) * 100))

