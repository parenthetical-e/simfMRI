def design_matrix(trials=[],impulses=None):
	"""
 	Uses <trials> (a list of integers) to create a 2d array, where each col 
	in that array matches one of the unique (sorted) entry in trials.
	
	If <impulses> is None it assumes that you want a binomial (boxcar) matrix.  
	
	If <impulses> is not None a parametric design matrix is created based on
	the elements in <impulses>.
	"""
	import numpy as np

	cond_levels = sort(list(set(trials))) 
		## Find and sort unique trials, aka condition levels
		
	trials = np.array(trials) 
	impulses = np.array(impulses)
	
	if trials.shape[0] != impulses.shape[0]:
		raise IndexError('trials and impulses and different lengths')

	# Gen the impulse and hrf convolved
	# dm and row-wise truncate the latter.
	dm = np.zeros(trials.shape[0],len(cond_levels))
	if impulses == None:
		impulses = [1,] * len(trials)
	
	for cond in cond_levels:
		cond_mask = cond == trials
		if (cond == 0) or (cond == '0'):
			dm[cond,cond_mask] = 1
				## Cond 0 is ALWAYS baseline and is ALWAYS 1
		else:
			dm[cond,cond_mask] = impulses[cond_mask]
	
	return dm