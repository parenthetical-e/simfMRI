import numpy as np

import simfMRI
import simBehave
import rl

from simfMRI.base import Fmri

class RW(Exp):
	""" 
	Generate and fit behavioral data with a Rescorla-Wagner RL model. 
	Use these to run a series of fMRI simulations  This class defines a 
	single experiment.  Many models may be examined inside a single 
	experiment.
	"""
	def __init__(behave='learn'):
		Exp.__init__(self,trials=[],data={},TR=2,ISI=2)
		
		n_cond = 1
		n_trials_cond = 60
		trials = []; acc = []; p = []
		if self.behave == 'learn':
			trials,acc,p = simBehave.behave.learn(
					n_cond,n_trials_cond,3,True)
		elif self.behave == 'random':
			trials,acc,p = simBehave.behave.random(
					n_cond,n_trials_cond,3,True)
		else:
			raise ValueError(
					'{0} is not known.  Try learn or random.'.format(behave))
		
		
		# Find best RL learning parameters for the behavoiral data
		# then generate the final data and unpack it into a list.
		best_rl_pars, best_logL = rl.fit.ml_delta(acc,trials,0.05)
		v_dict, rpe_dict = rl.reinforce.b_delta(acc,trials,best_rl_pars[0])
		values = rl.misc.unpack(v_dict,trials)
		rpes = rl.misc.unpack(rpe_dict,trials)
		
		# Store the results in appropriate places
		self.trials = trials
		self.data['n_cond'] = n_cond
		self.data['n_trials_cond'] = n_trials_cond
		self.data['acc'] = acc
		self.data['p'] = p
		self.data['best_logL'] = best_logL
		self.data['best_rl_pars'] = best_rl_pars
		self.data['values'] = values
		self.data['rpes'] = rpes
	
	
	def model_1():
		pass
		
	
