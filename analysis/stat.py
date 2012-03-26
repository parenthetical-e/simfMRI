import numpy as np
import bigstats as bs
from simfMRI.io import read_hdf_inc

def summary(hdf,model):
	""" 
	For <model>, return a statistical summary of the <hdf> 
	containing the results. 
	"""

	# Get the meta data for model
	meta_bold = read_hdf_inc(hdf,model+'/data/meta/bold').next()
	meta_dm = read_hdf_inc(hdf,model+'/data/meta/bold').next()

	# Get M and SD for t,p,bic
	# Do all calculations online.
	pass 


def overlap(hdf,cond1,cond2):
	""" 
	Calculates the overlap betwwen <cond1> and <cond2> for each model in the
	results list.
	"""

	pass

