#! /usr/opt/local/python
""" fMRI and behavioral/rl experiments."""
import os
import cPickle
import numpy as np
from scikits.statsmodels.api import GLS
from collections import defaultdict
import datetime

# Mine:
import rl
import simBehave
import simfMRI


def run(n_iter,n_cond,n_trials):
	"""
	A event related BOLD simulation experiment, with a single condition, 
	compare fits to a noisy simulated BOLD timecourse between the canonical 
	unit impulse HRF to HRF models derived from Rescorla-Wagner RL models.  

	The simulation of behavioral learning has been made more realistic.
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

		## Create RL data rl.ml_fit() 
		## then the final data and unpack it.
		pars, logL = rl.fit.ml_delta(acc,trialset,0.05)
		v_dict,rpe_dict = rl.reinforce.b_delta(acc,trialset,pars[0])
		values = rl.misc.unpack(v_dict,trialset)
		rpes = rl.misc.unpack(rpe_dict,trialset)
		
		data['rl_par'].append(pars)
		data['logL'].append(logL)

		## Create design matrices, 
		## univariate then parametric
		# design_matrix(conditions=[],impulses=None)
		unit_dm1,unit_dm2 = simfMRI.fmri.design_matrix(trialset,None)
		values_dm1,values_dm2 = simfMRI.fmri.design_matrix(trialset,values)
		rpes_dm1,rpes_dm2 = simfMRI.fmri.design_matrix(trialset,rpes)
		acc_dm1,acc_dm2 = simfMRI.fmri.design_matrix(trialset,acc)
		rand_dm1,rand_dm2 = simfMRI.fmri.design_matrix(
				trialset,np.random.rand(len(trialset)))

		## Make BOLD.
		len_noise = unit_dm2.shape[0]
		unit_bold = unit_dm2[:,1] + simfMRI.fmri.noise(len_noise,'white')
		values_bold = values_dm2[:,1] + simfMRI.fmri.noise(len_noise,'white')
		rpes_bold = rpes_dm2[:,1] + simfMRI.fmri.noise(len_noise,'white')
		acc_bold = acc_dm2[:,1] + simfMRI.fmri.noise(len_noise,'white')

		## Fit GLM
			# unit_dm2[:,0] is the baseline model
		print('X is 0:base,1:unit,2:values,3:rpes,4:acc,5:rand,6:dummy')
		dummy = np.array([1]*unit_bold.shape[0]) # *_bold are 1d
		X = np.vstack((
				unit_dm2[:,0],unit_dm2[:,1],values_dm2[:,1],
				rpes_dm2[:,1],acc_dm2[:,1],rand_dm2[:,1],dummy))
		ZX = simfMRI.fmri.dm_Z(X)
		na_msk = np.isnan(ZX)
		ZX[na_msk] = X[na_msk]
			# Replace NaNs with the original values...
			# This is not a god general solution, of course,
			# but Z-scores result from division by the std dev
			# which is 0 only when x is 0 or a repeat of 
			# the same vue.  The repeat case is likely the dummy
			# which need to be left as is.
		ZX = np.transpose(ZX)
		glm_unit = GLS(unit_bold,ZX).fit()
		glm_values = GLS(values_bold,ZX).fit()
		glm_rpes = GLS(rpes_bold,ZX).fit()
		glm_acc = GLS(acc_bold,ZX).fit()

		data['ZX'].append(ZX)
		data['glm_unit'].append(glm_unit)
		data['glm_values'].append(glm_values)
		data['glm_rpes'].append(glm_rpes)
		data['glm_acc'].append(glm_acc)

	## Write the data; build the name then use it
	time_code = datetime.datetime.now().strftime("%m%d%Y@%H%M%S")
	exp_conds = 'i'+str(n_iter) + 'c'+str(n_cond)+ 't'+str(n_trials)
	f_name = 'delta_rand_learn_' + exp_conds + '_' + time_code + '.pkl'
	print('Simulation complete, saving data to {0}'.format(f_name))
	fid = open(f_name,'wb')
	cPickle.dump(data,fid)
	fid.close()

	return data

