#! /usr/opt/local/python
""" fMRI and behavioral/rl experiments."""
import os
import h5py
import numpy as np
from scikits.statsmodels.api import GLS
from collections import defaultdict

import rl
import simBehave
import simfMRI

class Exp():
	def __init__(self,N,k,behave='learn'):
		# User defined parameters
		self.pars.n_cond = N
		self.pars.n_trials = k		
		self.pars.behave = behave
		
		# Hard coded parameters
		self.pars.noise = 'white'
		self.pars.param_resolution = 0.05
		
		# Initialize the results and/or simulation- 
		# state attributes
		self.length = N*k		
		self.trialset = []
		self.acc = []
		self.p = []
		
		self.dm = np.array([])
		self.bold = np.array([])
		self.model = None
		
		self.best_rl_pars = None 
		self.best_logL = None
		self.values = []
		self.rpes = []
		
		# Where everything that will be returned ends up:
		self.results = {}
		
		# TODO adjust behave p_acc so it is like devel
		
		# Create the behavoiral data that will be used to create
		# the fMRI data.
		if self.pars.behave == 'learn':
			self.trialset,self.acc,self.p = simBehave.behave.learn(
					self.pars.n_cond,self.pars.n_trials,3,True)
		elif self.pars.behave == 'random':
			self.trialset,self.acc,self.p = simBehave.behave.random(
					self.pars.n_cond,self.pars.n_trials,3,True)
		else:
			raise ValueError(
					'{0} is not known.  Try learn or random.'.format(behave))
		
		# Find best RL learning parameters for the behavoiral data
		# then generate the final data and unpack it into a list.
		self.best_rl_pars, self.best_logL = rl.fit.ml_delta(
				self.acc,self.trialset,self.pars.param_resolution)
		v_dict, rpe_dict = rl.reinforce.b_delta(
				self.acc,self.trialset,self.best_rl_pars[0])
		self.values = rl.misc.unpack(v_dict,self.trialset)
		self.rpes = rl.misc.unpack(rpe_dict,self.trialset)
	
	
	def create_dm(self,kind=''):
		""" Sets X to the specified design matrix kind. """
		from simfMRI.exp_parallel import dm
		if kind == 'boxcar':
			dm._dm_boxcar()
		elif kind == 'value':
			dm._dm_value()
		elif kind == 'rpe':
			dm._dm_rpe()
		elif kind == 'random':
			dm._dm_random()
		else:
			raise ValueError('{0} was not understood.'.format(kind))
	
	
	def create_bold(self,cols=[1,]):
		""" 
		Uses the design matrix (dm) and noise parameters to create and
		set the BOLD signal. 
		"""
		
		# By row add cols from dm, 1d and Nd 
		# require seperate treatment
		dm_cols = self.dm[:,cols]
		if dm_cols.ndim == 1:
			self.bold = dm_cols
		else:
			self.bold = dm_cols.mean(1)
		
		# Now add noise
		self.bold += simfMRI.fmri.noise(self.bold.shape[0],self.pars.noise)
	
	
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
		return model_results
	
	
	def create_results(self,dm_name=''):
		# TODO: how to get all attrs and save them
		
		self.results['batch_code'] = self.batch_code
		self.results['length'] = self.length
		self.results['trialset'] = self.trialset
		self.results['p'] = self.p
		self.results['acc'] = self.acc
		
		self.results['best_rl_pars'] = self.best_rl_pars
		self.results['best_logL'] = self.best_logL
		self.results['values'] = self.values
		self.results['rpes'] = self.rpes
		
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
		
		dm_to_simulate = ('boxcar','value','rpe','random')
		for dm_name in dm_to_simulate:
			self.create_dm(kind=dm_name)
			self.dm = simfMRI.fmri.dm_Z(self.dm)
			self.create_bold(cols=[1,])
			self.fit(model='GLS')
			self.create_results(dm_name=dm_name)
 		
 		return self.results
