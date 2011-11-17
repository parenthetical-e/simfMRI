"""Misc helper functions for simfMRI experiments and their data."""
import numpy as np

def repack_glm(results, glm_name):
	"""
	Unpack and repack select fields of the named (glm object) in a 
	simfMRI.exp results object. The repacked_glm is a dict whose 
	values are 1d or 2d lists of data.
	"""
	from collections import defaultdict

	repacked_glms = defaultdict(list)
	for glm in results[glm_name]:
		repacked_glms['beta'].append(glm.params)
		repacked_glms['t'].append(glm.tvalues)
		repacked_glms['p'].append(glm.pvalues)
		repacked_glms['ci'].append(glm.conf_int())
		repacked_glms['resid'].append(glm.resid)
	
	return repacked_glms


def repack_X(results):
	"""
	Using a results object from simfMRI.exp,repack each column 
	in each entry in X into single columns, keyed on the original
	column number.  Facilitates plotting ofX data.  
	For histograms, pair with flatten_results()
	"""
	from collections import defaultdict

	repacked_X = defaultdict(list)
	xi_col_index = range(results['X'][0].shape[1])
	for xi in results['X']:
		[repacked_X[col].append(xi[:,col]) for col in xi_col_index]

	return repacked_X


def flatten_results(results,data_name):
	"""
	Unpacks and flattens a dict (results) assuming its values 
	are 1 or 2d lists. Facilitates hitogram creation.
	"""

	data = results[data_name]
	try:
		data = [item for sublist in data.values() for item in sublist]
		print('{0} is a dict, flattening its values.'.format(data_name))
	except TypeError:
		data = data.values() # Assume 1d 
	except AttributeError:
		try:
			data = [item for sublist in data for item in sublist]
			print('{0} is a (now flat) list.'.format(data_name))
		except TypeError:
			data = list(data) # assume 1d already, force type

	return data
