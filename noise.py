""" Noise models. """
import numpy as np
import scipy.stats as stats
from simfMRI.misc import process_prng


def white(N, prng=None):
    """ Create and return a white noise array of length <N>.
    
    Notes on prng:
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


def ar1(N, alpha=0.2, prng=None):
    """ Create AR1 noise (of length <N>, and strength <alpha>), based on 
    a white noise stream. 
    
    Te default of alpha of 0.2 was taken from the 'temporalnoise.R' function
    in the R 'neuRosim' package (ver 02-10):
    
    http://cran.r-project.org/web/packages/neuRosim/index.html 
    
    Notes on prng:
    If <prng> is a np.random.RandomState() instance, it is used for random
        number generation.  
    If <prng> is a number that number is used to seed (i.e., 
        RandomState(<prng>)).
    If <prng> is None, the seed is set automagically. """
    
    if (alpha > 1) or (alpha < 0):
        raise ValueError("alpha must be between 0-1.")
    
    prng = process_prng(prng)
    
    noise, prng = white(N, prng)
    arnoise = [noise[0], ]
        ## Init by copying over the first
        ## so the loop below
        ## has someting to work with for
        ## the first iteration
        
    [arnoise.append(noise[ii]+(alpha * noise[ii-1])) for ii in range(
            1, len(noise))]
    
    return arnoise, prng
    
 
def physio(N, TR, sigma=1, freq_heart=1.17, freq_resp=0.2, prng=None):
    """ Create periodic physiological noise of length N based on 
    <freq_heart> and <freq_resp> and a white noise process. 
    
    This function was ported form a similar function ('physnoise.R')
    in the R 'neuRosim' package (ver 02-10):
    
    http://cran.r-project.org/web/packages/neuRosim/index.html
    
    Notes on prng:
    If <prng> is a np.random.RandomState() instance, it is used for random
        number generation.  
    If <prng> is a number that number is used to seed (i.e., 
        RandomState(<prng>)).
    If <prng> is None, the seed is set automagically. """
    
    # Calculate rates
    heart_beat = 2 * np.pi * freq_heart * TR
    resp_rate = 2 * np.pi * freq_resp * TR
    
    # Use rate to make periodic heart 
    # and respiration (physio) drift 
    # timeseries
    t = np.arange(N)
    hr_drift = np.sin(heart_beat * t) + np.cos(resp_rate * t)
    
    # Renormalize sigma using the 
    # sigma of the physio signals
    hr_weight = sigma / np.std(hr_drift)
    
    # Create the white noise then
    # add the weighted physio
    noise, prng = white(N, prng) 
    noise += hr_weight * hr_drift
    
    return noise, prng

       
def shift(noise, offset, prng=None):
    """ Shift <noise> (1d) by <offset>.  If <white> is true add white 
    noise as well. 
    
    <prng> is a dummy included to keep things consistent with the other
    noise function's returns. """
    
    if offset < 0:
        raise ValueError("offset must be 0 or greater.")
    
    if noise.ndim > 1:
        raise IndexError("arr must be 1d.")
    
    # Use offset to shit noise, 
    # calling the result offnoise.
    offnoise = np.zeros_like(noise)  ## Init
    offnoise[(0+offset):] = noise[(0+offset):]
    
    return offnoise, prng



def onef(N, fraction, prng=None):
    """ Given some <noise> (1d array), add autocorrelations approximating
    a typical 1/f fMRI distribution.
    
    TODO Say more about 1/f parameters here. 
    
    Notes on prng:
    If <prng> is a np.random.RandomState() instance, it is used for random
        number generation.  
    If <prng> is a number that number is used to seed (i.e., 
        RandomState(<prng>)).
    If <prng> is None, the seed is set automagically. """
    
    raise NotImplementedError("TODO")

