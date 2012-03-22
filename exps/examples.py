import simfMRI
import numpy as np
from simfMRI.template import Exp

class Simple(Exp):
	""" Run <n> one condition experiments. Return a list of results. """
	def __init__(self,n):
		try: Exp.__init__(self)
		except AttributeError: pass
		
		self.trials = np.array([0,]*n + [1,]*n)
		np.random.shuffle(self.trials)

	def model_1(self):
		""" A very simple example model. """

		from simfMRI.dm import construct

		self.create_dm('boxcar',True)
		self.create_bold(self.dm[:,1],False)

		self.dm = self.normalize_f(self.dm)
		self.bold = self.normalize_f(self.bold)

		self.fit()
	

class TwoCond(Exp):
	"""
	Simulate two conditions suing one then the other as the BOLD signal
	"""
	def __init__(self,trials=[],data={},TR=2,ISI=2):
		try: Exp.__init__(self)
		except AttributeError: pass
		
		# 2 conditiom, 60 trial per condition
		trials,acc,p = simBehave.behave.random(2,60,True)
		self.trials = trials
	
	
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
