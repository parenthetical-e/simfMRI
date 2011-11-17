""" A set of plotting routines for simfMRI.exp results objects"""
import matplotlib.pyplot as plt

import simfMRI.misc

def hist_t_delta(results,glm_name,acc_col=4,rpe_col=3,val_col=2,rand_col=5):
	
	glm_data = simfMRI.misc.repacked_glm(results,glm_name)
	
	close(); 
	

#close(); hist(acctvals[:,4],normed=True,bins=100,alpha=.7,color='gray'); hist(acctvals[:,2],normed=True,bins=100,alpha=.7,color='blue'); hist(acctvals[:,3],normed=True,bins=100,alpha=.7,color='green'); hist(acctvals[:,5],normed=True,bins=100,alpha=.7,color='purple'); axvline(x=2.015,color='red',linewidth=4); xlabel('t values (of regression constants)'); ylabel('Counts (Blue: value, Green: RPE, Purple: random, Gray: simple)')

#close(); hist(simfMRI.misc.flatten_results(ry,4),normed=True,bins=100,alpha=.7,color='gray'); hist(simfMRI.misc.flatten_results(ry,2),normed=True,bins=100,alpha=.7,color='blue'); hist(simfMRI.misc.flatten_results(ry,3),normed=True,bins=100,alpha=.7,color='green'); ylim((0,1)); xlabel('Simulated BOLD'); ylabel('Counts (Blue: value, Green: RPE, Gray: simple)')


#close();  hist(values,bins=100,alpha=.7,normed=True); hist(rpes,bins=100,alpha=.7,normed=True); ylim(0,1); xlabel('Impulse magnitude'); ylabel('Blue: value, Green: RPE, Simple is binomial (not shown)')
