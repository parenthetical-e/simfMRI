#! /usr/opt/local/python
""" A base class for fMRI simulations."""
import os
import h5py
import numpy as np
from scikits.statsmodels.api import GLS
from collections import defaultdict

import simBehave
import simfMRI

class Exp():
	def __init__(self,N,k,behave='learn'):
		# User defined parameters
		self.n_cond = N
		self.n_trials = k		
		self.behave = behave

		# Hard coded parameters
		self.noise = 'white'
		self.dm_to_simulate = ('boxcar',)
		self.col_for_bold = [1,]
		
		# The normalization function is:
		self.normalize_f = simfMRI.fmri.dm_Z
		
		# Initialize the results and/or simulation- 
		# state attributes
		self.length = N*k		
		self.trialset = []
		self.acc = []
		self.p = []
		
		self.dm = np.array([])
		self.bold = np.array([])
		self.model = None
		
		# Where everything that will be returned ends up:
		self.results = {}
		
		# TODO adjust behave p_acc so it is like devel
		
		# Create the behavoiral data that will be used to create
		# the fMRI data.
		if self.behave == 'learn':
			self.trialset,self.acc,self.p = simBehave.behave.learn(
					self.n_cond,self.n_trials,3,True)
		elif self.behave == 'random':
			self.trialset,self.acc,self.p = simBehave.behave.random(
					self.n_cond,self.n_trials,3,True)
		else:
			raise ValueError(
					'{0} is not known.  Try learn or random.'.format(behave))
	
	
	def create_dm(self,kind=''):
		""" Sets X to the specified design matrix kind. """
		from simfMRI.exp_parallel import dm
		if kind == 'boxcar':
			dm._dm_boxcar(self)
		else:
			raise ValueError('{0} was not understood.'.format(kind))
	
	
	def create_bold(self):
		""" 
		Uses the design matrix (dm) and noise parameters to create and
		set the BOLD signal. 
		"""
		
		dm_cols = self.dm[:,self.col_for_bold]
		if dm_cols.ndim == 1:
			self.bold = dm_cols
		else:
			self.bold = dm_cols.mean(1)
		
		# Now add noise
		self.bold += simfMRI.fmri.noise(self.bold.shape[0],self.noise)
	
	
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
	
	
	def fit(self,model='GLS'):
		if model == 'GLS':
			self.model = GLS(self.bold,self.dm).fit()
		else:
			raise ValueError(
					'{0} was not understood.  Try GLS.'.format(model))
	
	
	def run(self,code):
		"""
		Go!
		"""
		self.batch_code = str(code)
		
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
