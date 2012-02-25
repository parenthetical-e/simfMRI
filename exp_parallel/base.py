#! /usr/opt/local/python
""" fMRI and behavioral/rl experiments."""
import os
import h5py
import numpy as np
from scikits.statsmodels.api import GLS
from collections import defaultdict
import datetime

# Mine:
import rl
import simBehave
import simfMRI

class Exp(code,n_cond,n_trials):
	def __init__(self,code,n_iter,n_cond,n_trials):
		self.code = str(code)
		self.n_cond = n_cond
		self.n_trials = n_trials
		
		self.trialset = []
		self.acc = []
		self.p = []
		self.values = []
		self.rpes = []
		
		self.dm = np.array()
		self.bold = np.array()
		
	
	def create_behave(kind='learn'):		
		if kind == 'learn':
			trialset,acc,p = simBehave.behave.learn(
					n_cond,n_trials,3,True,True)		
		elif kind == 'random':
			trialset,acc,p = simBehave.behave.random(
					n_cond,n_trials,3,True,True)
		else:
			raise ValueError(
					'{0} it not known.  Try learn or random.'.format(kind))
	
	
	def create_rl(param_resolution=0.05):
		## Find best RL learning parameters for the data 
		## generate the final data and unpack it into a list.
		self.pars, self.logL = rl.fit.ml_delta(
				self.acc,self.trialset,param_resolution)
		v_dict, rpe_dict = rl.reinforce.b_delta(
				self.acc,self.trialset,self.self.pars[0])
		self.values = rl.misc.unpack(self.v_dict,self.trialset)
		self.rpes = rl.misc.unpack(self.rpe_dict,self.trialset)
	
	
	def create_dm(kind=''):
		""" Sets X to the specified design matrix kind. """
		if kind == 'boxcar':
			self._dm_boxcar()
		elif kind == 'value':
			self._dm_value()
		elif kind == 'rpe':
			self._dm_rpe()
		elif kind == 'random':
			self._dm_random()
		else
			raise ValueError('{0} was not understood.'.format(kind))
	
	
	def _dm_boxcar():
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)	
		self.dm = dm_hrf
		
	def	_dm_value():
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)	
		dm_param, dm_param_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.values)
		dm_acc,dm_acc_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.acc)
		dummy = np.array([1]*dm.shape[0])
		self.dm = np.vstack((
				dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
				dm_hrf[:,1],dummy))
	
	def	_dm_rpe():
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)	
		dm_param, dm_param_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.rpes)
		dm_acc,dm_acc_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.acc)
		dummy = np.array([1]*dm.shape[0])
		self.X = np.vstack((
				dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
				dm_hrf[:,1],dummy))
		
	def	_dm_random():
		dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)	
		dm_param, dm_param_hrf = simfMRI.fmri.design_matrix(
				trialset,np.random.rand(len(trialset)))
		dm_acc,dm_acc_hrf = simfMRI.fmri.design_matrix(
				self.trialset,self.acc)
		dummy = np.array([1]*dm.shape[0])
		self.X = np.vstack((
				dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
				dm_hrf[:,1],dummy))	
	
	
	def create_bold(cols=[2],noise='white'):
		""" Uses X to create and set the BOLD signal. """
		
		self.bold = self.dm[:,cols] + simfMRI.fmri.noise(
				self.dm.shape[0],noise)
	
	
	def reformat_model(model):
		""" Extract relevant data from a regression model object. """
		

	
	def fit(model='GLS'):
		if model = 'GLS':
			self.model = GLS(self.bold,np.transpose(self.dm)).fit()
		
		
	def run(n):
		"""
		Go!
		"""
			
		self.create_behave(kind='learn')
		self.create_rl(param_resolution=0.05)
		
		results = {}
		results['index'] = n
		results['trialset'] = self.trialset
		results['p'] = self.p
		results['acc'] = self.acc
		results['values'] = self.values
		results['rpes'] = self.rpes
		
		dm_to_simulate = ('boxcar','value','rpe','random')
		for dm_name in dm_to_simulate:
			self.create_dm(kind='learn')
			self.dm = simfMRI.fmri.dm_Z(self.dm)
			self.create_bold(cols=[2],noise='white')
			self.fit(model='GLS')
			model_dict = self.reformat_model()
			for k,v in model_dict.items():
				results[k] = v
			
		return results
