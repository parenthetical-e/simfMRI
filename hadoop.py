""" Tools to allow simfMRI to be used in the Hadoop map-reduce framework. """

import numpy as mp
from collections import defaultdict

class ReduceER(results):
	""" A reducer class for ERfMRI. """
	def ___init___(self):
		# Create a reduced version of the results keys
		self.reduced_results = {}
		pass
	
	def reduce():
		# TODO 
		# For each value for each key in results 
		# calculate M and Var (online), update N too.
		# 
		# Maintain the structure of results
		# http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#cite_note-3		
		pass
	
