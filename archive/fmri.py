"""
Functions to facilitate fMRI (BOLD timecourse) monte-carlo simulations.
"""
import os
import numpy as np
import simfMRI


def design_matrix(conditions=[],impulses=None):
	"""
	Creates and returns two design matrices (dm) based on conditions and 
	impulses (if provided).
	
	dm_1 is just a mapping from conditions to columns in the dm, while 
	the second is the first column-wise  convolved with double_gamma().  
	"""

	
	conditions = list(conditions) # force, just in case.
	cond_levels = list(set(conditions)) # Find unique conditions

	dm_1 = np.zeros((len(conditions),len(cond_levels)))
	dm_2 = np.zeros_like(dm_1) 
		# init

	## Gen the impulse and hrf convolved
	## dm and row-wise truncate the latter.
	if impulses == None:
		impulses = []
		for cond in conditions:
			if (cond == 0) | (cond == '0'):
				impulses.append(0.0)
			else:
				impulses.append(1.0)

	for ii,cond in enumerate(conditions):
		dm_1[ii,cond] = impulses[ii]

	for col_num in range(dm_1.shape[1]):
		bold = simfMRI.convolve.w_double_gamma(dm_1[:,col_num]) 
		dm_2[:,col_num] = bold[0:dm_1.shape[0]]

	return dm_1,dm_2


def design_matrix_hrf_params(conditions=[],impulses=None,hrf_params=dict()):
	"""
	Creates and returns two design matrices (dm) based on conditions and 
	impulses (if provided).
	
	dm_1 is just a mapping from conditions to columns in the dm, while 
	the second is the first column-wise  convolved with 
	param_double_gamma(), which relies on hrf_params.  
	"""
	
	conditions = list(conditions) # force, just in case.
	cond_levels = list(set(conditions)) # Find unique conditions

	dm_1 = np.zeros((len(conditions),len(cond_levels)))
	dm_2 = np.zeros_like(dm_1) 
		# init

	## Gen the impulse and hrf convolved
	## dm and row-wise truncate the latter.
	if impulses == None:
		impulses = []
		for cond in conditions:
			if (cond == 0) | (cond == '0'):
				impulses.append(0.0)
			else:
				impulses.append(1.0)

	for ii,cond in enumerate(conditions):
		dm_1[ii,cond] = impulses[ii]

	## Preturb a randomly slected cannonical HRF
	## parameter.  Use those hrf_params in the convolvution.
	for col_num in range(dm_1.shape[1]):
		bold = simfMRI.convolve.w_param_double_gamma(
				dm_1[:,col_num],**hrf_params)
		dm_2[:,col_num] = bold[0:dm_1.shape[0]]

	return dm_1,dm_2


def noise(N, noise_type):
	"""
	Create and return a noise array of length N.

	noise_type
		white: Guassian, M=0, SD=1
	
	"""
	import scipy.stats as stats

	if noise_type == 'white':
		noise = stats.norm.rvs(size=N)
	else:
		raise ValueError, 'noise_type was unknown: {0}'.format(name)

	return noise 
		# a np.array()
		

def dm_Z(design_matrix):
	"""
	Z-scores, then returns, each column in design_matrix.
	"""
	import numpy as np

	## Get the Z-scores
	# x is original, y is transformed,
	# u is the column mean, 
	# s is the column standard deviation
	# repeat for each row (i) and column (j):
	# 	y_i_j = (x_i_j - u_j) / s_j
	c_mean = design_matrix.mean(0)
	c_std = design_matrix.std(0)
	dm_Z = (design_matrix - c_mean) / c_std
	
	return dm_Z


def dm_percent(design_matrix):
	"""
	Calculates, then returns, percent change for each column in 
	design_matrix.
	"""

	# x is original, y is transformed,
	# u is the column mean
	# repeat for each row (i) and column (j):
	# 	y_i_j = 100 + ((x_i_j - u_j)/u_j) * 100
	c_mean = design_matrix.mean(0)
	dm_P = np.nan_to_num(100 + (((design_matrix-c_mean)/c_mean) * 100))
	
	return dm_P

