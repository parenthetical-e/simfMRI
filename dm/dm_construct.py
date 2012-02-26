""" Private design matrix constructors """
import numpy as np
import simfMRI
from simfMRI.dm.base import design_matrix

def _dm_boxcar(self):
	dm, dm_hrf = design_matrix(self.trials,None)
	self.dm = dm_hrf


def	_base_box_acc_dummy(self):
	dm_box = design_matrix(self.trials,None)
	dm_acc = design_matrix(self.trials,self.data.['acc'])
	dummy = np.array([1]*dm.shape[0])
	self.dm = np.vstack((dm_box[:,0],dm[:,1],dm_acc[:,1],dummy))


def	_base_box_value_dummy(self):
	dm_box = design_matrix(self.trials,None)
	dm_value = design_matrix(self.trials,self.data.['value'])
	dummy = np.array([1]*dm.shape[0])
	self.dm = np.vstack((dm_box[:,0],dm[:,1],dm_value[:,1],dummy))


def	_base_box_rpe_dummy(self):
	dm_box = design_matrix(self.trials,None)
	dm_rpe = design_matrix(self.trials,self.data.['rpe'])
	dummy = np.array([1]*dm.shape[0])
	self.dm = np.vstack((dm_box[:,0],dm[:,1],dm_rpe[:,1],dummy))
	

def	_base_box_rand_dummy(self):
	dm_box = design_matrix(self.trials,None)
	dm_rand = = design_matrix(self.trials,np.random.rand(len(self.trials)))
	dummy = np.array([1]*dm.shape[0])
	self.dm = np.vstack((dm_box[:,0],dm[:,1],dm_rand[:,1],dummy))

