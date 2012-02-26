def design_matrix(trials=[],impulses=None):
	"""
	Creates and returns two design matrices (dm) based on trials and 
	impulses (if provided).
	
	dm is just a mapping from trials to columns in the dm, while 
	the second is the first column-wise  convolved with double_gamma().  
	"""

	
	trials = list(trials) # force, just in case.
	cond_levels = list(set(trials)) # Find unique trials

	dm = np.zeros((len(trials),len(cond_levels)))
	dm_2 = np.zeros_like(dm) 
		# init

	## Gen the impulse and hrf convolved
	## dm and row-wise truncate the latter.
	if impulses == None:
		impulses = [1,] * len(trials)
	
	for ii,cond in enumerate(trials):
		if cond == 0:
			dm[ii,cond] = 1
		else:
			dm[ii,cond] = impulses[ii]
	
	return dm