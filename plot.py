""" A set of plotting routines for simfMRI.exp results objects"""
import matplotlib.pyplot as plt
import numpy as np
import simfMRI

# frac overlap, howto calc?
# quant how?
	# mean beta w/ CI?
	# boxplot instead?
	# Asses noise effect how?

# code to do plots of hrf/raw data
# what does the corr w acc tell us
	# anything that generalizes?

# make sure unit is as it should be.  The complete lack of corr with value id odd, esp for t90

# do with td (3 state)
# do with rc

def hist_t_delta(results,glm_name):
	
	glm_data = simfMRI.misc.repack_glm(results,glm_name)
	tvalues = np.array(glm_data['t'])

	plt.rcParams['font.size'] = 16
	fig = plt.figure()
	ax = fig.add_subplot(111)

	# X is 0:base,1:unit,2:values,3:rpes,4:acc,5:rand,6:dummy
	dataloc = [1,4,2,3,5]
	labels = ['Unit','Accuracy','Value','RPE','Random']
	colors = ['black','orange','green','blue','purple']
	hist_params = dict(bins=50,histtype='stepfilled',alpha=0.4)
	for lc,lb,co in zip(dataloc,labels,colors):
		print(lc,lb,co)
		ax.hist(tvalues[:,lc],label=lb,color=co,**hist_params)
	
	ax.axvline(x=2.015,label='p < 0.05',color='red',linewidth=3)
	ax.axvline(x=3.36493,label='p < 0.01',color='red',linewidth=2)
	ax.axvline(x=4.03214,label='p < 0.005',color='red',linewidth=1)

	ax.set_xlabel('t-values')
	ax.set_ylabel('Counts')
	plt.xlim(-10,15)
	plt.ylim(0,90)
	plt.legend(bbox_to_anchor=(1.10, 1.10))

	plt.show()

#close(); hist(simfMRI.misc.flatten_results(ry,4),normed=True,bins=100,alpha=.7,color='gray'); hist(simfMRI.misc.flatten_results(ry,2),normed=True,bins=100,alpha=.7,color='blue'); hist(simfMRI.misc.flatten_results(ry,3),normed=True,bins=100,alpha=.7,color='green'); ylim((0,1)); xlabel('Simulated BOLD'); ylabel('Counts (Blue: value, Green: RPE, Gray: simple)')


#close();  hist(values,bins=100,alpha=.7,normed=True); hist(rpes,bins=100,alpha=.7,normed=True); ylim(0,1); xlabel('Impulse magnitude'); ylabel('Blue: value, Green: RPE, Simple is binomial (not shown)')
