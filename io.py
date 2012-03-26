""" Functions for reading and writing of Exp results """
import h5py
import numpy as np
	
def _walk(d,hdf):
	""" 
	Recursively walk the provided dict <d> creating groups or saving data 
	in <hdf>, as appropriate.
	"""
	for k,v in d.items():
		if isinstance(v, dict):
			# print('\n-----\n\n{0}: dict, creating a group'.format(k))
			hdfnext = hdf.create_group(k)
			_walk(v,hdfnext)
				## gettin' all recursive and shit, yo.
		else:
			if v is None: v = 0
				## h5py does not know 
				## what to do with None.
			
			data = np.array(v)
			# print('{0}: data'.format(k))
			hdfd = hdf.create_dataset(k,data=data)


def write_hdf(results,name):
	""" 
	Iterate over the results list, mimicking the hierarchical structure of 
	each entry.  Name the resulting file <name>.
	"""
	from simfMRI.io import _walk
	
	f = h5py.File(name,'w')
	for ii,r in enumerate(results):
		# Create a top level group for each r
		# in results.  Then recursively walk r.
		# Anything that is not a dict is 
		# assumed to be data.		
		fg_ii = f.create_group(str(ii))
		_walk(r,fg_ii)
	
	f.close()


def read_hdf(hdf,path='/model_01/t'):
	""" 
	In the <hdf> file, for every top-level node return the 
	data specified by path.
	"""

	# First locate the dataset in the first result,
	# then grab that data for every run.
	f = h5py.File(hdf,'r')

	return [f[node+path].value for node in f.keys()]


def read_hdf_inc(hdf,path='/model_01/t'):
	""" 
	In the <hdf> file, for every top-level node *incrementally* return the 
	data specified by path.
	"""

	# First locate the dataset in the first result,
	# then grab that data for every run.
	f = h5py.File(hdf,'r')

	for node in f.keys():
		yield f[node+path].value


def get_model_meta(hdf,model):
	""" Get the BOLD and DM metadata for <model> from <hdf> """

	f = h5py.File(hdf,'r')

	meta = {}
	meta['bold'] = f['/0/'+ model +'/data/meta/bold'].value
	meta['dm'] = f['/0/'+ model +'/data/meta/dm'].value.tolist()

	return meta

