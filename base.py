import numpy as np
from collections import defaultdict

import simfMRI

# fmri
# - convert trial/states/etc - preprocess, make dms
# - define BOLD, add noise
# - do regressions

class Fmri():
	""" A class for running easily parallelizable fMRI simulations. """
	
	def __init__(self,trials=[],data={},TR=1,ISI=1):
		# Set up user variables
		self.TR = TR
		self.ISI = ISI
		self.trials = trials
		self.data = data
		
		# Intialize simulation data structues
		self.dm = None
		self.bold = None
		self.model = None
		self.results = {}
		
		# Define needed functions
		self.noise_f = simfMRI.noise.white
		self.normalize_f = simfMRI.norm.zscore
		self.basis_f = simfMRI.hrf.double_gamma
		self.basis_params = {width:32,TR:1,a1:6.0,a2:12.,b1:0.9,b2:0.9,c:0.35}
		
		# Move from ISI to ITI time, if needed.
		if (self.ISI % self.TR) > 0.0:
			raise ValueError('ISI must a even multiple of the TR.')
		elif self.ISI > self.TR:
			from copt import deepcopy
			# Use multplier to transform data and trials into units
			# of TR from their native ISI.
			mult = self.ISI/self.TR
			
			trials_copy = deepcopy(self.trials)
			trials_mult = []
			[self.trials_mult.extend([t,] + [0,]*(mult-1)) for 
					t in trials_copy]
			
			data_copy = deepcopy(self.data)
			data_mult = defaultdict(list)
			for k,vals in data_copy.items():
				[data_mult[k].extend([v,] + [0,]*(mult-1)) for v in vals]
	
			self.trials = trials_mult
			self.data = data_mult
	
	
	def convolve_hrf(self,arr):
		"""
		Convolves hrf basis with a 1 or 2d (column-oriented) array.
		"""
		
		basis = self.basis_f(**self.basis_params)
		
		arr = np.asarray(arr)
		arr_c = np.zeros_like(arr)
		try:
			for ii in range(arr.shape[1]):
				arr_c[:,ii] = np.convolve(arr[:,ii],basis)[0:arr.shape[0]]
		except IndexError:
			arr_c = np.convolve(arr[:],basis)[0:arr.shape[0]]
		
		return arr_c
	
	
	def create_dm(self,kind='',convolve=True):
		""" Use trials to return a design matrix. """
		
		""" Sets X to the specified design matrix kind. """
		from simfMRI.dm import dm_construct
		if kind == 'boxcar':
			dm_construct._dm_boxcar(self)
		else:
			raise ValueError('{0} was not understood.'.format(kind))
		
		if convolve:
			self.dm = self.convolve_hrf(self.dm)
	
	
	def create_bold(self,arr):
		""" Use only trials ans data to simulate bold signal """
		self.bold = arr += self.noise_f(len(arr))
	
	
	def reformat_model(self):
		"""
		Extract relevant data from a regression model object into a dict.
		"""
		
		model_results = {}
		model_results['beta'] = self.model.params
		model_results['t'] = self.model.tvalues
		model_results['fvalue'] = self.model.fvalue
		model_results['p'] = self.model.pvalues
		model_results['r'] = self.model.rsquared
		model_results['ci'] = self.model.conf_int()
		model_results['resid'] = self.model.resid
		model_results['aic'] = self.model.aic
		model_results['bic'] = self.model.bic
		model_results['llf'] = self.model.llf
		model_results['mse_model'] = self.model.mse_model
		model_results['mse_resid'] = self.model.mse_resid
		model_results['mse_total'] = self.model.mse_total
		model_results['pretty_summary'] = self.model.summary()
		
		return model_results
	
	
	def create_results(self,dm_name=''):
		# TODO: how to get all attrs and save them
		
		self.results['batch_code'] = self.batch_code
		self.results['length'] = self.length
		self.results['trialset'] = self.trialset
		self.results['p'] = self.p
		self.results['acc'] = self.acc
		
		
		model_dict = {}
		model_dict = self.reformat_model()
		model_dict['dm'] = self.dm
		model_dict['bold'] = self.bold
		
		self.results[dm_name] = {}
		for k,v in model_dict.items():
			self.results[dm_name][k] = v
	
	
	def fit(self):
		""" Calculate the regression parameters and statistics. """
		from scikits.statsmodels.api import GLS
		
		self.model = GLS(self.Y,self.X).fit()
	
