""" Who knows what, really.  The miscellaneous goes here."""

def preturb_double_gamma(percent):
	"""
	Add scaled (by percent) white noise to a randomly selected double gamma
	HRF parameter.  Return a dict of HRF parameters.
	"""
	import scipy.stats as stats
	
	params = {a1:6.0,a2:12.0,b1:0.9,b2:0.9,c:0.35}
	
	keys = params.keys()
	np.random.shuffle(keys) # inplace
	par = params[keys[0]]
	params[keys[0]] = stats.norm.rvs(loc=par,scale=par/(1./percent))
		## Grab a random value from the normal curve
		## with its SD reduced by 0.percent
	
	params('width') = 32
	params['TR'] = 1
		## Add the remaining (unpreturbed) params
	
	return params

