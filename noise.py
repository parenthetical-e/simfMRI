""" Noise models. """
import numpy as np
import scipy.stats as stats
from simfMRI.misc import process_prng


def white(N, prng=None):
    """ Create and return a noise array of length <N>.
    If <prng> is a np.random.RandomState() instance, it is used for random
        number generation.  
    If <prng> is a number that number is used to seed (i.e., 
        RandomState(<prng>)).
    If <prng> is None, the seed is set automagically. """
    
    prng = process_prng(prng)
    
    np.random.set_state(prng.get_state())
        ## Pass random state from prng to np so that
        ## stats.<> will inherit the irght state.
        ## There does not seem to be a way to set random
        ## state of stats.* functions directly.
    
    noise = stats.norm.rvs(size=N)
    
    prng.set_state(np.random.get_state())
        ## Pass the seed stat from np back to
        ## prng, then we can use prng again...
    
    return noise, prng
