""" Private design matrix constructors """
import numpy as np
import simfMRI

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
	self.dm = np.vstack((
			dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
			dm_hrf[:,1],dummy))

def	_dm_random(self):
	dm, dm_hrf = simfMRI.fmri.design_matrix(self.trialset,None)
	dm_param, dm_param_hrf = simfMRI.fmri.design_matrix(
			self.trialset,np.random.rand(len(self.trialset)))
	dm_acc,dm_acc_hrf = simfMRI.fmri.design_matrix(
			self.trialset,self.acc)
	dummy = np.array([1]*dm.shape[0])
	self.dm = np.vstack((
			dm_hrf[:,0],dm_param_hrf[:,1],dm_acc_hrf[:,1],
			dm_hrf[:,1],dummy))