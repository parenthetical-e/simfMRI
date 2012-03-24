""" Custom design matrix constructors """
import numpy as np
import simfMRI
from simfMRI.dm.base import design_matrix
from simfMRI.norm import zscore
# FYI
# design_matrix(onsets=[],durations=None,impulses=None):

# For template.py
def boxcar(self):
	return design_matrix(self.trials,None,None)

# =========
# for simfMRI.exps.rl.RW
# =========
def	base_box_acc(self):
	dm_box = design_matrix(self.trials,None,None)
	dm_acc = zscore(design_matrix(self.trials,None,self.data['acc']))
	return np.vstack((dm_box[:,0],dm_box[:,1],dm_acc[:,1])).transpose()


def	base_box_value(self):
	dm_box = design_matrix(self.trials,None,None)
	dm_value = zscore(design_matrix(self.trials,None,self.data['value']))
	return np.vstack((dm_box[:,0],dm_box[:,1],dm_value[:,1])).transpose()


def	base_box_rpe(self):
	dm_box = design_matrix(self.trials,None,None)
	dm_rpe = zscore(design_matrix(self.trials,None,self.data['rpe']))
	return np.vstack((dm_box[:,0],dm_box[:,1],dm_rpe[:,1])).transpose()
	

def	base_box_rand(self):
	dm_box = design_matrix(self.trials,None,None)
	dm_rand = zscore(design_matrix(self.trials,None,
			np.random.rand(len(self.trials))))
	return np.vstack((dm_box[:,0],dm_box[:,1],dm_rand[:,1])).transpose()

