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


def noisy_double_gamma(width):
	"""
	Returns a HRF (and its free parameters) after it randomly selects one 
	of the free params from the cannonical double_gamma() adding white 
	noise to it, centered around either:
		a1: 6.0
		a2: 12.0
		b2: .9
		c: .35
	"""
	import scipy.stats as stats
	from math import fabs 
		# absolute value

	hrf = []
	x = np.arange(width)
	
	## Randomly pick a key/param and 
	## add noise, then calc the HRF.
	params = dict(a1=6, a2=12.0, b2=0.9, c=0.35)
	keys = params.keys()
	np.random.shuffle(keys) # inplace
	par = params[keys[0]]
	params[keys[0]] = stats.norm.rvs(loc=par,scale=par/4.)
		# Add white noise scaled to 1/2 of loc
		# fabs() taken to prevent any of the params 
		# dropping below zero, which would be bad.
		# Give the scale limitation this should only
		# rarely, if ever, bias the sampling; I hope anyway.
	
	## HRF:
	a1 = params['a1']
	a2 = params['a2']
	b2 = params['b2']
	b1 = b2
	c = params['c']
	d1 = a1*b1
	d2 = a2*b2
	f = lambda x: (x/d1)**a1 * np.exp( (d1-x)/ b1) - c * (x/d2)**a2 *\
			np.exp( (d2-x)/ b2)
	[hrf.append(f(ii)) for ii in x] 

	return np.array(hrf), params

