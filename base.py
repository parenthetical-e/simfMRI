import numpy as np
from collections import defaultdict

# fmri
# - convert trial/states/etc - preprocess, make dms
# - define BOLD, add noise
# - do regressions

class Fmri(N,trials,data,TR,ISI):
	""" A class for running easily parallelizable fMRI simulations. """
	
	def __init__(self,N,trials=[],data={},TR=1,ISI=1):
		self.N = N	## The model number, a code.
		self.TR = TR
		self.ISI = ISI
		
		if (self.ISI % self.TR) > 0.0:
			raise ValueError('ISI must a even multiple of the TR.')
		elif self.ISI > self.TR:
			# Use multplier to transform data and trials into units
			# of TR from their native ISI.
			multplier = self.ISI/self.TR
			
			self.trials = []
			for t in trials:
				self.trials.extend([t,]*multplier)
			
			self.data = defaultdict(list)
			for k,vals in data.items():
				[data[k].extend([v,]*multplier) for v in vals]
		else:
			self.trials = trials
			self.data = data
		
		self.basis = None
		self.conds = None
		self.X = None
		self.Y = None
		self.results = defaultdict(list)
		# ....

	
	def _convolve_hrf(self,dm):
		"""
		Convolves hrf basis with a 1 or 2d (column-oriented) array.
		"""
		
		basis = self.basis
		dm_c = np.zeros_like(dm)
		try:
			for ii in range(dm.shape[1]):
				dm_c[:,ii] = np.convolve(dm[:,ii],basis)[0:dm.shape[0]]
		except IndexError:
			dm_c = np.convolve(dm[:],basis)[0:dm.shape[0]]
		
		return dm_c
	

	def dm(self,add=[0,1],convolve=True):
		""" Use trials to return a design matrix. """
		
		dm = np.zeros((len(self.trials),len(add)))
		for ii,x in enumerate(self.trials):
			try:
				add.index(x)
			except ValueError:
				continue
			
			dm[ii,x] = 1
		
		if convolve:
			self.X = self._convolve_hrf(dm)
		else:
			self.X = dm
		
		self.conds = add
		self.conds.sort()
	

	def p_dm(self,add={0:None,1:'rpe',2:'rpe'},convolve=True):
		""" Use data and trials to return a parametric design matrix. """
		
		pass
		# HOW TO do this?  Map trials to data how?
		# give each col a name in a sep list
		
		# return pdm
	

	def norm(self,kind='Z'):
		""" 
		Normalizes X and Y. Defaults to Z-scores ('Z').  Percent change is 
		also available ('Percent').
		"""
		from simfMRI.norm import zscore, percent_change
		
		if kind == 'Z':
			self.Y = zscore(self.Y)
			self.X = zscore(self.X)
		elif (kind == 'Percent') or (kind == 'percent'):
			self.Y = percent_change(self.Y)
			self.X = percent_change(self.X)
	

	def hrf(self,params):
		"""
		Create the a double gamma HRF basis. Defaults are the canonical
		parameters.
		"""
		from simfMRI.hrf import double_gamma
		
		self.basis = double_gamma(**params)
	
	
	def bold(self,legend):
		""" Use only trials ans data to simulate bold signal """
		bold = []
		# do stuff
		
		self.Y = bold
	
	
	def fit(self):
		""" Calculate the regression parameters and statistics. """
		from scikits.statsmodels.api import GLS
		
		self.model = GLS(self.Y,self.X).fit()
	
	
	def format_results(self):
		"""
		Reformats the model's results into a more accessible dictionary.
		"""
		
		self.results['beta'] = model.params
		self.results['t'] = model.tvalues
		self.results['fvalue'] = model.fvalue
		self.results['p'] = model.pvalues
		self.results['r'] = model.rsquared
		self.results['ci'] = model.conf_int()
		self.results['resid'] = model.resid
		self.results['aic'] = model.aic
		self.results['bic'] = model.bic
		self.results['llf'] = model.llf
		self.results['mse_model'] = model.mse_model
		self.results['mse_resid'] = model.mse_resid
		self.results['mse_total'] = model.mse_total
	

	def save_results(self,delim=','):
		""" Write the results to text files (in /results), one per entry. """
		import sys
		
		# TODO mkdir results if needed
		
		for k,vals in self.results.items():
			# Write each, stepping over ducks.
			pass
	

