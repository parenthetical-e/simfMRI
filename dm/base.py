def design_matrix(trials=[],impulses=None):
	"""
 	Uses <trials> (a list of integers) to create a 2d array, where each col 
	in that array matches one of the unique (sorted) entry in trials.
	
	If <impulses> is None it assumes that you want a binomial (boxcar) matrix.  
	
	If <impulses> is not None a parametric design matrix is created based on
	the elements in <impulses>.
	"""

	
	trials = list(trials) 
	impulses = list(impulses)
		## force, just in case.
	
	if len(trials) != len(impulses):
		raise IndexError('trials and impulses and different lengths')
	
	cond_levels = sort(list(set(trials))) 
		## Find and sort unique trials, aka condition levels

	## Gen the impulse and hrf convolved
	## dm and row-wise truncate the latter.
	dm = np.zeros((len(trials),len(cond_levels)))
	if impulses == None:
		impulses = [1,] * len(trials)
	
	for ii,cond in enumerate(trials):
		if cond == 0:
			dm[ii,cond] = 1
				## Column 0 is ALWAYS baseline
		else:
			dm[ii,cond] = impulses[ii]
	
	return dm