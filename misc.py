""" Who knows what, really.  The miscellaneous goes here."""
import numpy as np


def preturb_double_gamma(fraction,width,TR):
	"""
	Add scaled (by <fraction> (0-1)) white noise to a randomly selected double 
	gamma HRF parameter.  Returns a dict of HRF parameters.
	
	<width> and <TR> are not used here but are needed for HRF calculations 
	downstream.
	"""
	import scipy.stats as stats
	
	params = {a1:6.0,a2:12.0,b1:0.9,b2:0.9,c:0.35}
		## The conanoical parameters
	
	keys = params.keys()
	np.random.shuffle(keys)
	par = params[keys[0]]
	params[keys[0]] = stats.norm.rvs(loc=par,scale=par/(1.*fraction))
		## Grab a random value from the normal curve
		## with its SD reduced by 0.fraction
	
	params['width'] = width
	params['TR'] = TR
		## Add the remaining (unpreturbed) params
	
	return params


def process_prng(prng):
    """ See if <prng> is a numpy.random.RandomState object. 
    If it is return it.  If not, try and create one by 
    RandomState(<prng>), which will work of prng was 
    None or a number. """

    # See if prng is a RandomState (and so has
    # a state to get) or create a RandomState
    # overriding prng
    try:
        prng.get_state()
    except AttributeError:
        print("Creating new RandomState(). Seed: {0}".format(prng))
        prng = np.random.RandomState(prng)
    
    return prng

