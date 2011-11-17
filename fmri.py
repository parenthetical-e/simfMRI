"""
Functions to facilitate fMRI (BOLD timecourse) monte-carlo simulations.
"""
import os
import numpy as np
import simfMRI


def design_matrix(conditions=[],impulses=None):
	"""
	Creates and returns two design matrices (dm), where each condition in 
	conditions becomes a column in the new dm.  
	
	dm_1 is the impuluse response version (0,1) i.e. a binary mapping from 
	conditions to the dm, while the second is the first column-wise 
	convolved with double_gamma() truncated to the same length as dm_1.
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
				impulses.extend(0.0)
			else
				impulses.extend(1.0)

	for ii,cond in enumerate(conditions):
		dm_1[ii,cond] = impulses[ii]

	for col_num in range(dm_1.shape[1]):
		bold = simfMRI.convolve.w_double_gamma(dm_1[:,col_num]) # defined below
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

