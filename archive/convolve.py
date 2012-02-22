""" Create BOLD models."""
import numpy as np
import simfMRI

def w_double_gamma(impulses):
	"""
	Convolves impulses, a 1 or 2d (column-oriented) array, 
	with the double gamma hemodynamic response function (hrf).  
	"""

	hrf = simfMRI.hrf.double_gamma(20)
	n_col = 0
	try: 
		n_col =	impulses.shape[1]
	except IndexError:
		n_col = 1 
			# impulses is likely 1d
	except AttributeError:
		n_col = 1
		print('Impulses is not an array. Assume it is 1d.')
	
	if n_col == 1:
		return np.convolve(impulses,hrf)
	else:
		bold = np.zeros_like(impulses)
		for ii in range(n_col):

			bold[:,ii] = np.convolve(
					impulses[:,ii],hrf)[0:impulses.shape[0]]
		return bold


def w_param_double_gamma(impulses,a1,a2,b2,c):
	"""
	Convolves impulses, a 1 or 2d (column-oriented) array, 
	with the double gamma hemodynamic response function (hrf).

	Canonical parameters are a1=6, a2=12.0, b2=0.9, and c=0.35.
	"""
	## This is a seperate function from w_double_gamma to 
	## preserve backwards compatibility.

	hrf = simfMRI.hrf.param_double_gamma(20,a1,a2,b2,c)
	n_col = 0
	try: 
		n_col =	impulses.shape[1]
	except IndexError:
		n_col = 1 
			# impulses is likely 1d
	except AttributeError:
		n_col = 1
		print('Impulses is not an array. Assume it is 1d.')
	
	if n_col == 1:
		return np.convolve(impulses,hrf)
	else:
		bold = np.zeros_like(impulses)
		for ii in range(n_col):

			bold[:,ii] = np.convolve(
					impulses[:,ii],hrf)[0:impulses.shape[0]]
		return bold

