#! /usr/opt/local/python
""" fMRI and behavoiral/rl experiments."""
import os
import cPickle
import numpy as np
from scikits.statsmodels.api import GLS
from collections import defaultdict
import datetime

import rl
import simBehave
import simfMRI


def run(n_iter,n_cond,n_trials):
	"""
	A event related BOLD simulation experiment, with a single condition, 
	compare fits to a noisy simulated BOLD timecourse between the cononical 
	unit impulse HRF to HRF models derived from Rescorla-Wagner RL models.  

	One of the four free HRF parameters is randomly perturbed in the BOLD 
	timecourse simulation of acc (only). In thie version acc is the only 
	ground truth.
	"""

	data = defaultdict(list)
		# create a dict the defaults to an 
		# empty list for unkown keys

	for ii in range(n_iter):
		print('Iteration {0}.'.format(ii))
		data['index'].append(ii)

		# all_learn(N,k,loc,event,rand_learn)
		trialset,acc,p = simBehave.behave.all_learn(
				n_cond,n_trials,3,True,True)
		
		data['trialset'].append(trialset)
		data['acc'].append(acc)
		data['p'].append(p)

		## Create RL data rl.ml_fit() 
		## then the final data and unpack it.
		pars, logL = rl.fit.ml_delta(acc,trialset,0.05)
		v_dict,rpe_dict = rl.reinforce.b_delta(acc,trialset,pars[0])
		values = rl.misc.unpack(v_dict,trialset)
		rpes = rl.misc.unpack(rpe_dict,trialset)
		
		data['rl_par'].append(pars)
		data['logL'].append(logL)
		data['values'].append(values)
		data['rpes'].append(rpes)

		## Create design matrices, 
		## univariate then parametric
		params = dict(a1=6, a2=12.0, b2=0.9, c=0.35)
		perturbed_params = simfMRI.hrf.preturb_params(
				dict(a1=6, a2=12.0, b2=0.9, c=0.35))
				# Canonical paramters

		dm = simfMRI.fmri.design_matrix_params
			# rename for readability

		unit_dm1,unit_dm2 = dm(trialset,None,params)
		values_dm1,values_dm2 = dm(trialset,values,params)
		rpes_dm1,rpes_dm2 = dm(trialset,rpes,params)
		acc_dm1,acc_dm2 = dm(trialset,acc,perturbed_params)
		rand_dm1,rand_dm2 = dm(
				trialset,np.random.rand(len(trialset)),params)

		## Make BOLD.		
		noise = simfMRI.fmri.noise(unit_dm2.shape[0],'white')
		acc_bold = acc_dm2[:,1] + noise

		## Fit GLM
			# unit_dm2[:,0] is the baseline model
		print('X is 0:base,1:unit,2:values,3:rpes,4:acc,5:rand,6:dummy')
		dummy = np.array([1]*acc_bold.shape[0]) # *_bold are 1d
		X = np.vstack((
				unit_dm2[:,0],unit_dm2[:,1],values_dm2[:,1],
				rpes_dm2[:,1],acc_dm2[:,1],rand_dm2[:,1],dummy))
		X = np.transpose(X)
		glm_acc = GLS(acc_bold,X).fit()

		data['X'].append(X)
		data['glm_acc'].append(glm_acc)
			## Becausei of the singlar pertubation
			## onyl calc and keep glm_acc

	## Write the data; build the name then use it
	time_code = datetime.datetime.now().strftime("%m%d%Y@%H%M%S")
	exp_conds = 'i'+str(n_iter) + 'c'+str(n_cond)+ 't'+str(n_trials)
	f_name = ('delta_rand_learn_param_hrf_acc' + exp_conds + '_' 
			+ time_code + '.pkl')
	print('Simulation complete, saving data to {0}'.format(f_name))
	fid = open(f_name,'wb')
	cPickle.dump(data,fid)
	fid.close()

	return data




