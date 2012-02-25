#! /usr/opt/local/python
""" fMRI and behavioral/rl experiments."""
import os
import h5py
import numpy as np
from scikits.statsmodels.api import GLS
from collections import defaultdict
import datetime

import rl
import simBehave
import simfMRI

class Exp():
	def __init__(self,N,k,behave='learn'):
		self.n_cond = N
		self.n_trials = k
		self.length = N*k
		
		self.dm = np.array([])
		self.bold = np.array([])
		
		# Create the behavoiral data that will be used to create
		# the fMRI data.
		self.trialset = []
		self.acc = []
		self.p = []
		if behave == 'learn':
			self.trialset,self.acc,self.p = simBehave.behave.learn(
					self.n_cond,self.n_trials,3,True)
		elif behave == 'random':
			self.trialset,self.acc,self.p = simBehave.behave.random(
					self.n_cond,self.n_trials,3,True)
		else:
			raise ValueError(
					'{0} is not known.  Try learn or random.'.format(behave))
		
		
		# Find best RL learning parameters for the behavoiral data
		# then generate the final data and unpack it into a list.
		self.param_resolution = 0.05
		self.values = []
		self.rpes = []
		self.pars, self.logL = rl.fit.ml_delta(
				self.acc,self.trialset,self.param_resolution)
		v_dict, rpe_dict = rl.reinforce.b_delta(
				self.acc,self.trialset,self.pars[0])
		self.values = rl.misc.unpack(v_dict,self.trialset)
		self.rpes = rl.misc.unpack(rpe_dict,self.trialset)

	
	def create_dm(self,kind=''):
		""" Sets X to the specified design matrix kind. """
		if kind == 'boxcar':
			self._dm_boxcar()
		elif kind == 'value':
			self._dm_value()
		elif kind == 'rpe':
			self._dm_rpe()
		elif kind == 'random':
			self._dm_random()
		else:
			raise ValueError('{0} was not understood.'.format(kind))
	
	
	def _dm_boxcar(self):
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)
		self.dm = dm_hrf
	
	def	_dm_value(self):
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)
		dm_param, dm_param_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.values)
		dm_acc,dm_acc_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.acc)
		dummy = np.array([1]*dm.shape[0])
		self.dm = np.vstack((
				dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
				dm_hrf[:,1],dummy))
	
	def	_dm_rpe(self):
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)
		dm_param, dm_param_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.rpes)
		dm_acc,dm_acc_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.acc)
		dummy = np.array([1]*dm.shape[0])
		self.X = np.vstack((
				dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
				dm_hrf[:,1],dummy))
	
	def	_dm_random(self):
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)
		dm_param, dm_param_hrf = simfMRI.fmri.design_matrix(
				trialset,np.random.rand(len(trialset)))
		dm_acc,dm_acc_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.acc)
		dummy = np.array([1]*dm.shape[0])
		self.X = np.vstack((
				dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
				dm_hrf[:,1],dummy))
	
	
	def create_bold(self,cols=[1],noise='white'):
		""" Uses X to create and set the BOLD signal. """
		
		self.bold = self.dm_hrf[:,cols] + simfMRI.fmri.noise(
				self.dm_hrf.shape[0],noise)
	
	
	def reformat_model(model):
		""" Extract relevant data from a regression model object. """
		
		model_results = {}
		model_results['beta'] = model.params
		model_results['t'] = model.tvalues
		model_results['fvalue'] = model.fvalue
		model_results['p'] = model.pvalues
		model_results['r'] = model.rsquared
		model_results['ci'] = model.conf_int()
		model_results['resid'] = model.resid
		model_results['aic'] = model.aic
		model_results['bic'] = model.bic
		model_results['llf'] = model.llf
		model_results['mse_model'] = model.mse_model
		model_results['mse_resid'] = model.mse_resid
		model_results['mse_total'] = model.mse_total
		return model_results
	
	
	def fit(self,model='GLS'):
		if model == 'GLS':
			self.model = GLS(self.bold,np.transpose(self.dm)).fit()
	
	
	def run(self,code):
		"""
		Go!
		"""	
		self.batch_code = str(code)
		
		results = {}
		results['batch_code'] = self.batch_code
		results['trialset'] = self.trialset
		results['p'] = self.p
		results['acc'] = self.acc
		results['values'] = self.values
		results['rpes'] = self.rpes
		
		dm_to_simulate = ('boxcar','value','rpe','random')
		for dm_name in dm_to_simulate:
			self.create_dm(kind=dm_name)
			self.dm = simfMRI.fmri.dm_Z(self.dm)
			self.create_bold(cols=[1],noise='white')
			self.fit(model='GLS')
			
			model_dict = self.reformat_model()
			model_dict['dm'] = self.dm
			model_dict['bold'] = self.bold
			for k,v in model_dict.items():
				results[str.join(k,'_',dm_name)] = v
 		
 		return results
