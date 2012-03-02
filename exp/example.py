import simfMRI
from simfMRI.base import ERfMRI

class TwoCond(ERfMRI):
	"""
	Simulate two conditions suing one then the other as the BOLD signal
	"""
	def __init__(self,trials=[],data={},TR=2,ISI=2):
		super(TwoCond, self).__init__()
		
		# 2 conditiom, 60 trial per condition
		trials,acc,p = simBehave.behave.random(2,60,True)
		self.trial = trials
	
	
	def model_1(self):
		# Cond 1 is the BOLD
		self.create_dm('boxcar',True)
		self.create_bold(self.dm[:,1])
		
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
		
		self.fit()
	
	
	def model_2():
		# Cond 2 is the BOLD
		self.create_dm('boxcar',True)
		self.create_bold(self.dm[:,2])
		
		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)
		
		self.fit()
	

def sim(code):
	"""
	Carries out one simulation (with two models, model_1 and model_2).
	
	This code is to be invoked inside iPython.  
	
	However. This is just one way to do it... see also example_2.py.
	"""
	from simfMRI.exp.example import TwoCond
	
	# Create a TwoCond instance, using the defaults
	# and run it.
	print 'Running the simulation.'
	tci = TwoCond()
	results = tci.run(code)
	
	print 'Saving the results.'
	simfMRI.io.write_HDF(results)

	return results
	
