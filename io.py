""" Functions for reading and writing of Exp results """

def write_hdf(map_results_list):
	""" 
	Iterate over the list, using each key in the first dict to create datasets
	for all the values.  Mimic the hierarchical structure of results.
	"""
	import h5py
	
	f = h5py.File('simfMRI.hdf5')
	for r in map_results_list:
		pass
