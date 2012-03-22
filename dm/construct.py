""" Custom design matrix constructors """
import numpy as np
import simfMRI
from simfMRI.dm.base import design_matrix

# For template.py
def boxcar(self):
	return design_matrix(self.trials,None)


# =========
# for simfMRI.exps.rl.RW
# =========
def	base_box_acc(self):
	dm_box = design_matrix(self.trials,None)
	dm_acc = design_matrix(self.trials,self.data['acc'])
	return np.vstack((dm_box[:,0],dm[:,1],dm_acc[:,1]))


def	base_box_value(self):
	dm_box = design_matrix(self.trials,None)
	dm_value = design_matrix(self.trials,self.data['value'])
	return np.vstack((dm_box[:,0],dm[:,1],dm_value[:,1]))


def	base_box_rpe(self):
	dm_box = design_matrix(self.trials,None)
	dm_rpe = design_matrix(self.trials,self.data['rpe'])
	return np.vstack((dm_box[:,0],dm[:,1],dm_rpe[:,1]))
	

def	base_box_rand(self):
	dm_box = design_matrix(self.trials,None)
	dm_rand = design_matrix(self.trials,np.random.rand(len(self.trials)))
	return np.vstack((dm_box[:,0],dm[:,1],dm_rand[:,1]))

