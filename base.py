import re
import numpy as np
from copy import deepcopy
from collections import defaultdict

import simfMRI

# fmri
# - convert trial/states/etc - preprocess, make dms
# - define BOLD, add noise
# - do regressions

class Exp():
	"""
	A template class for running easily parallelizable event-related fMRI
	experimental simulations.
	"""
	
	def __init__(self,trials=[],data={},TR=2,ISI=2):
		import simfMRI
		
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
		self.basis_params = {
			'width':32,'TR':1,'a1':6.0,'a2':12.,'b1':0.9,'b2':0.9,'c':0.35}
		
		# Move from ISI to ITI time, if needed.
		if (self.ISI % self.TR) > 0.0:
			raise ValueError('ISI must a even multiple of the TR.')
		elif self.ISI > self.TR:
			# Use multplier to transform data and trials into units
			# of TR from their native ISI.
			mult = self.ISI/self.TR
			
			trials_copy = deepcopy(self.trials)
				## Needed to prevent circular updates
			trials_mult = []
			[self.trials_mult.extend([t,] + [0,]*(mult-1)) for
					t in trials_copy]
			
			data_copy = deepcopy(self.data)
			data_mult = defaultdict(list)
			for k,vals in data_copy.items():
				[data_mult[k].extend([v,] + [0,]*(mult-1)) for v in vals]
			
			# Finally replace results with the
			# expanded version
			self.trials = trials_mult
			self.data = data_mult
	
	
	def convolve_hrf(self,arr):
		"""
		Convolves hrf basis with a 1 or 2d (column-oriented) array.
		"""
		
		basis = self.basis_f(**self.basis_params)
		
		arr = np.asarray(arr)
		arr_c = np.zeros_like(arr)
			#@ Where the convolved data goes
		
		# Assume 2d (or really N > 1 d), fall back to 1d.
		try:
			for ii in range(arr.shape[1]):
				arr_c[:,ii] = np.convolve(arr[:,ii],basis)[0:arr.shape[0]]
		except IndexError:
			arr_c = np.convolve(arr[:],basis)[0:arr.shape[0]]
		
		return arr_c
	
	
	def create_dm(self,name='',convolve=True):
		"""
		Creates a design matrix (dm) using the constructors in
		simfMRI.dm.construct
		
		<name> - the name of the constructor you want use.
		<convolve> - if True, the dm is convolved with the HRF defined by
			self.basis_f().
		"""
		from simfMRI.dm import construct
		
		self.dm = getattr(construct,name)(self)
		if convolve:
			self.dm = self.convolve_hrf(self.dm)
	
	
	def create_bold(self,arr,convolve=True):
		""" The provided <arr>ay becomes a (noisy) bold signal. """
		
		self.bold = np.array(arr)
		self.bold += self.noise_f(self.bold.shape[0])
		if convolve:
			self.bold = self.convolve_hrf(self.bold)
		
	
	def _reformat_model(self):
		"""
		Use save_state() to store the simulation's state.*
		
		This private method just extracts relevant data from the regression
		model object into a dict.
		"""
		tosave = {
			'beta':'params',
			't':'tvalues',
			'fvalue':'fvalue',
			'p':'pvalues',
			'r':'rsquared',
			'ci':'conf_int',
			'resid':'resid',
			'aic':'aic',
			'bic':'bic',
			'llf':'llf',
			'mse_model':'mse_model',
			'mse_resid':'mse_resid',
			'mse_total':'mse_total',
			'pretty_summary':'summary'
		}
		
		# Try to get each attr (a value in the dict above)
		# first as function (without args) then as a regular
		# attribute.  If both fail, silently move on.
		model_results = {}		
		for k,v in tosave.items():
			try:
				model_results[k] = getattr(self.model,v)()
			except TypeError:
				model_results[k] = getattr(self.model,v)
			except AttributeError:
				continue
			
		return model_results
	
	
	def save_state(self,name):
		"""
		Saves most of the state of the current simulation to results, keyed
		on <name>.  Saves greedily, trading storage space for security and
		redundancy.
		"""
		
		tosave = {
			'TR':'TR',
			'ISI':'ISI',
			'trials':'trials',
			'data':'data',
			'dm':'dm',
			'bold':'bold'
		}
			## This list is only for attr hung directly off
			## of self.

		# Add a name to results
		self.results[name] = {}
		
		# Try to get each attr (a value in the dict above)
		# first as function (without args) then as a regular
		# attribute.  If both fail, silently move on.
		for k,v in tosave.items():
			try:
				self.results[name][k] = getattr(self,v)()
			except TypeError:
				self.results[name][k] = getattr(self,v)
			except AttributeError:
					continue
		
		# Now add the reformatted data from the current model,
		# if any.
		self.results[name].update(self._reformat_model()) 
	
	
	def fit(self):
		""" Calculate the regression parameters and statistics. """
		from scikits.statsmodels.api import GLS
		
		# Appends a dummy predictor and runs the regression
		#
		# Dummy is added at the last minute so it does not
		# interact with normalization or smooithng routines.
		dm_dummy = np.ones((self.dm.shape[0],self.dm.shape[1]+1))
		dm_dummy[0:self.dm.shape[0],0:self.dm.shape[1]] = self.dm
		
		self.model = GLS(self.bold,dm_dummy).fit()
	
	
	def contrast(contrast=np.array([])):
		"""
		Uses the current model to statistically compare predictors (t-test),
		returning t and p values.
		
		<contrast> - a list of {1,0,-1} the same length as the number
			of predictors in the model (sans the dummy).
		
		If <contrast> is 2d, each row is treated as a separate contrast.
		"""
		
		# TODO
		pass
		return t, p
	
	
	def model_1(self):
		""" A very simple example model. """
		
		from simfMRI.dm import construct
		
		self.create_dm('boxcar',True)
		self.create_bold(self.dm[:,1],False)
		
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
		
		self.fit()
	
	
	def run(self,code):
		"""
		Run all defined models in order, returning their tabulated results.
		
		<code> - the unique batch or run code for this experiment.
		
		Models are any attribute of the form 'model_N' where N is an
		integer (e.g. model_2, model_1012 or model_666).  Models take no
		arguments.
		"""
		
		self.results['batch_code'] = code
		
		# find all self.model_N attritubes and run them.
		all_attr = dir(self)
		all_attr.sort()
		
		for a in all_attr:
			a_s = re.split('_',a)
			if len(a_s) == 2:
				if (a_s[0] == 'model') and (re.match('\A\d+\Z',a_s[1])):
					amodel = getattr(self,a)
					amodel()
					self.save_state(name=a)
		
		return self.results
		