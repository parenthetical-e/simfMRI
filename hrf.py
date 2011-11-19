"""A collection of hemodynamic response functions."""
import numpy as np

def double_gamma(width):
	"""
	Returns a HRF using 'cannonical' parameters.
	"""

	hrf = []
	x = np.arange(width)
	a1 = 6.
	a2 = 12.
	b2 = .9
	b1 = b2
	c = .35
	d1 = a1*b1
	d2 = a2*b2
	f = lambda x: (x/d1)**a1 * np.exp( (d1-x)/ b1) - c * (x/d2)**a2 *\
			np.exp( (d2-x)/ b2)
	[hrf.append(f(ii)) for ii in x]

	return np.array(hrf)


def param_double_gamma(width,a1,a2,b2,c):
	"""
	Returns a HRF based on params. For canonical parameters use,
	(a1=6, a2=12.0, b2=0.9, c=0.35).
	"""

	## The independent params are provided,
	## calculate the dependent ones
	b1 = b2
	d1 = a1*b1
	d2 = a2*b2

	hrf = []
	x = np.arange(width)
	f = lambda x: (x/d1)**a1 * np.exp( (d1-x)/ b1) - c * (x/d2)**a2 *\
			np.exp( (d2-x)/ b2)
	[hrf.append(f(ii)) for ii in x]

	return np.array(hrf)


def preturb_params(params=dict(a1=6, a2=12.0, b2=0.9, c=0.35)):
	"""
	Add rescaled white noise to a randomly selected param.
	"""
	import scipy.stats as stats
	
	keys = params.keys()
	np.random.shuffle(keys) # inplace
	par = params[keys[0]]
	params[keys[0]] = stats.norm.rvs(loc=par,scale=par/4.)
		## Grab a random value from the normal curve
		## with its SD reduced by 0.25

	return params
