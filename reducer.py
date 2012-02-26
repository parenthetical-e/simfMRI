""" This function should reduce fMRI simulation results """
# TODO
class Reduce_fmri(results):
	def ___init___(self):
		# Create a reduced version of the results keys
		self.reduced_results.M = defaultdit(list)
		self.reduced_results.Var = defaultdit(list)
		self.reduced_results.N = defaultdit(list)
		pass
	
	def reduce():
		# For each value for each key in results 
		# calculate M and Var (online), update N too.
		pass
	
# http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#cite_note-3
