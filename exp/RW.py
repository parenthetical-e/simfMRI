import numpy as np

import simfMRI
from simfMRI.base import Fmri
	
def run(self,code):
	# TODO all the below is dated, cerate exp run file for devel
	
	"""
	Go!
	"""
	self.batch_code = str(code)
	# TODO redo for compat w devel
	
	for dm_name in self.dm_to_simulate:
		# Create dm, and bold
		# then norm them seperatly.
		self.create_dm(kind=dm_name)
		self.create_bold()
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
		self.fit(model='GLS')
		
		self.create_results(dm_name=dm_name)
	
	return self.results