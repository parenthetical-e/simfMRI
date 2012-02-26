"""Routines to normalize 1d and 2d array-like objects. """
import numpy as np

def zscore(arr):
	arr = np.array(arr)
	
	# x is original, y is transformed,
	# u is the column means 
	# s is the column std devs
	#
	# vectorizing.... 
	# repeat for each row (i) and column (j)
	# y_i_j = (x_i_j - u) / s		
	s = arr.std(0)
	u = arr.mean(0)
		
	return (arr - u) / s
	
def percent_change(arr):
	# x is original, y is transformed,
	# u is the column means
	# 
	# vectorizing....
	# repeat for each row (i) and column (j):
	# 	y_i_j = 100 + ((x_i_j - u_j)/u_j) * 100
	u = arr.mean(0)
	return np.nan_to_num(100 + (((arr-u)/u) * 100))

