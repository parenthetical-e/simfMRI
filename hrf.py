"""A collection of hemodynamic response functions."""
import numpy as np

def double_gamma(width=32,TR=1,a1=6.0,a2=12.,b1=0.9,b2=0.9,c=0.35):
	"""
	Returns a HRF.  Defaults are the canonical parameters.
	"""
	
	x_range = np.arange(0,width,TR)	
	d1 = a1*b1
	d2 = a2*b2
	
	# Vectorized
	hrf = ((x_range / d1) ** a1 * np.exp((d1 - x_range) / b1)) - (
			c * (x_range / d2) ** a2 *np.exp((d2 - x_range) / b2))
	
	return hrf
