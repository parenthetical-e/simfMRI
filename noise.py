def white(N):
	""" Create and return a noise array of length N. """
	import scipy.stats as stats

	return stats.norm.rvs(size=N)