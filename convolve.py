""" Create BOLD models."""
import numpy as np
import simfMRI

def w_double_gamma(impulses,noisy=False):
	"""
	Convolves impulses, a 1 or 2d (column-oriented) array, 
	with the double gamma hemodynamic response function (hrf).  
	"""
	if noisy:
		hrf = simfMRI.hrf.double_gamma(20)
		hrf_params = None
	else:
		hrf,hrf_params = simfMRI.noisy_double_gamma(20)

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
		return np.convolve(impulses,hrf), hrf_params
	else:
		bold = np.zeros_like(impulses)
		for ii in range(n_col):

			bold[:,ii] = np.convolve(
					impulses[:,ii],hrf)[0:impulses.shape[0]]
		return bold, hrf_params

