import numpy as np
import rl
import simfMRI
import simBehave
from simfMRI.template import Exp

class RW(Exp):
	"""
	Generate and fit behavioral data with a Rescorla-Wagner RL model. 
	Use the RPE and values from these fits to run fMRI simulations with
	parameteric regressors.
	"""
	def __init__(self,n,behave='learn'):
		Exp.__init__(self,TR=2,ISI=2)
		
		n_cond = 1
		n_trials_cond = n
		trials = []; acc = []; p = []
		if behave is 'learn':
			trials,acc,p = simBehave.behave.learn(
					n_cond,n_trials_cond,3,True)
		elif behave is 'random':
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
		self.data['acc'] = acc
		self.data['p'] = p
		self.data['best_logL'] = best_logL
		self.data['best_rl_pars'] = best_rl_pars
		self.data['value'] = values
		self.data['rpe'] = rpes
	

	# DEFINE ALL MODELS:
	def model_01(self):
		self.data['meta']['bold'] = 'condition 1'
		self.data['meta']['dm'] = ('baseline','condition 1')

		self.create_dm('boxcar',True)
		self.create_bold(self.dm[:,1],False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()
		
	
	def model_02(self):
		self.data['meta']['bold'] = 'condition 1'
		self.data['meta']['dm'] = ('baseline','condition 1','acc')

		self.create_dm('base_box_acc',True)
		self.create_bold(self.dm[:,1],False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()


	def model_03(self):
		self.data['meta']['bold'] = 'condition 1'
		self.data['meta']['dm'] = ('baseline','condition 1','value')

		self.create_dm('base_box_value',True)
		self.create_bold(self.dm[:,1],False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()

	
	def model_04(self):
		self.data['meta']['bold'] = 'condition 1'
		self.data['meta']['dm'] = ('baseline','condition 1','rpe')
		
		self.create_dm('base_box_rpe',True)
		self.create_bold(self.dm[:,1],False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()


	def model_05(self):
		self.data['meta']['bold'] = 'condition 1'
		self.data['meta']['dm'] = ('baseline','condition 1','rand')
		
		self.create_dm('base_box_rand',True)
		self.create_bold(self.dm[:,1],False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()


	def model_06(self):
		self.data['meta']['bold'] = 'acc'
		self.data['meta']['dm'] = ('baseline','condition 1','value')

		self.create_dm('base_box_value',True)
		
		self.create_bold(self.convolve_hrf(self.data['acc']),False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()


	def model_07(self):
		self.data['meta']['bold'] = 'acc'
		self.data['meta']['dm'] = ('baseline','condition 1','rpe')
	
		self.create_dm('base_box_rpe',True)
		
		self.create_bold(self.convolve_hrf(self.data['acc']),False)
	
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
	
		self.fit()
	
	
	def model_08(self):
		self.data['meta']['bold'] = 'acc'
		self.data['meta']['dm'] = ('baseline','condition 1','rand')
	
		self.create_dm('base_box_rand',True)
		
		self.create_bold(self.convolve_hrf(self.data['acc']),False)
	
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
	
		self.fit()
	
	
	def model_09(self):
		self.data['meta']['bold'] = 'value'
		self.data['meta']['dm'] = ('baseline','condition 1','rpe')
	
		self.create_dm('base_box_rpe',True)
		
		self.create_bold(self.convolve_hrf(self.data['value']),False)
	
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
	
		self.fit()
	
	
	def model_10(self):
		self.data['meta']['bold'] = 'rpe'
		self.data['meta']['dm'] = ('baseline','condition 1','value')
	
		self.create_dm('base_box_value',True)
		
		self.create_bold(self.convolve_hrf(self.data['rpe']),False)
	
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
	
		self.fit()
	

	def model_11(self):
		self.data['meta']['bold'] = 'rand'
		self.data['meta']['dm'] = ('baseline','condition 1','acc')

		self.create_dm('base_box_acc',True)
		
		randarr = np.zeros(len(self.trials))
		for ii,t in enumerate(self.trials):
			if t >= 1: 
				randarr[ii] = np.random.rand(1)
		
		# print (np.array(self.trials) > 0.0) == (randarr > 0.0)
				
		self.create_bold(self.convolve_hrf(randarr),False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()


	def model_12(self):
		self.data['meta']['bold'] = 'rand'
		self.data['meta']['dm'] = ('baseline','condition 1','value')

		self.create_dm('base_box_value',True)

		randarr = np.zeros(len(self.trials))
		for ii,t in enumerate(self.trials):
			if t >= 1: 
				randarr[ii] = np.random.rand(1)

		# print (np.array(self.trials) > 0.0) == (randarr > 0.0)

		self.create_bold(self.convolve_hrf(randarr),False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()


	def model_13(self):
		self.data['meta']['bold'] = 'rand'
		self.data['meta']['dm'] = ('baseline','condition 1','rpe')

		self.create_dm('base_box_rpe',True)

		randarr = np.zeros(len(self.trials))
		for ii,t in enumerate(self.trials):
			if t >= 1: 
				randarr[ii] = np.random.rand(1)

		# print (np.array(self.trials) > 0.0) == (randarr > 0.0)

		self.create_bold(self.convolve_hrf(randarr),False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()

