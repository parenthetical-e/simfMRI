#! /usr/opt/local/python
""" 
A subclass for fMRI simulations of parametric models.
"""
import os
import h5py
import numpy as np
from scikits.statsmodels.api import GLS
from collections import defaultdict

import simBehave
import simfMRI
from simfMRI.exp_parallel.base import Exp


class RW(Base):
	""" A subclass studying simulated Rescorla-Wagner RL models."""
	def __init__(self,N,k,behave='learn'):
        Exp.__init__(self,N,k,behave='learn')
		
		# RW attributes			
		self.param_resolution = 0.05
		self.best_rl_pars = None 
		self.best_logL = None
		self.values = []
		self.rpes = []
		
		# Find best RL learning parameters for the behavoiral data
		# then generate the final data and unpack it into a list.
		self.best_rl_pars, self.best_logL = rl.fit.ml_delta(
				self.acc,self.trialset,self.pars.param_resolution)
		v_dict, rpe_dict = rl.reinforce.b_delta(
				self.acc,self.trialset,self.best_rl_pars[0])
		self.values = rl.misc.unpack(v_dict,self.trialset)
		self.rpes = rl.misc.unpack(rpe_dict,self.trialset)
	
	
	# There are new attributes.  Overide.
	def create_results(self,dm_name=''):		
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
	
	
	# Override to extend understood kinds
	def create_dm(self,kind=''):
		""" Sets X to the specified design matrix kind. """
		from simfMRI.exp_parallel import dm
		if kind == 'boxcar':
			dm._dm_boxcar(self)
		elif kind == 'value':
			dm._dm_value(self)
		elif kind == 'rpe':
			dm._dm_rpe(self)
		elif kind == 'random':
			dm._dm_random(self)
		else:
			raise ValueError('{0} was not understood.'.format(kind))		