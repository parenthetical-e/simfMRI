def design_matrix(onsets=[],durations=None,impulses=None):
	"""
 	Uses <onsets> and maybe <durations> to create a 2d array, where each col 
 	matches one of the unique (sorted) entry in onsets.  
	
	If <durations> is None, it is assumed that you want a event related desgin.

	If <impulses> is None it assumes that you want a binomial (boxcar) matrix.  
	If <impulses> is not None a parametric design matrix is created based on
	the magnitude of each entry in <impulses>.
	"""
	import numpy as np
	
	if impulses is None:
		impulses = np.ones(len(onsets))
	
	if durations is None:
		durations = np.zeros(len(onsets))
			## A duration of 0 give a 
			## single spike at onset.

	cond_levels = list(set(onsets))
	cond_levels.sort()
		## Find and sort unique onsets, 
		## aka condition levels
		
	onsets = np.array(onsets)
	impulses = np.array(impulses)
	durations = np.array(durations)
	if onsets.shape[0] != durations.shape[0]:
		raise IndexError('onsets and durations and different lengths')

	if onsets.shape[0] != impulses.shape[0]:
		raise IndexError('onsets and impulses and different lengths')

	# Gen the impulse and hrf convolved
	# dm and row-wise truncate the latter.
	dm = np.zeros((onsets.shape[0]+np.sum(durations),len(cond_levels)))
		## The number of row is equal to the number of onsets 
		## plus the sum of durations.  

	# Expand onsets and impulses to match the durations
	# specified in durations
	onsets_x = []
	impulses_x = []
	if np.sum(durations) >= 1:
		# Expand then convert to arrays.
		[onsets_x.append([o,]*(d+1)) for o,d in zip(onsets,durations)]
		[impulses_x.append([i,]*(d+1)) for i,d in zip(impulses,durations)]
		onsets_x = np.array(onsets_x)
		impulses_x = np.array(impulses_x)
	else:
		# Just copy them over
		onsets_x = onsets[:]
		impulses_x = impulses[:]

	for cond in cond_levels:
		cond_mask = cond == onsets_x
		if cond == 0:
			dm[cond_mask,cond] = 1
				## Cond 0 is ALWAYS baseline and is ALWAYS 1
		else:
			dm[cond_mask,cond] = impulses_x[cond_mask]
	
	return dm