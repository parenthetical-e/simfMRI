"""A collection of hemodynamic response functions."""
import numpy as np
import scipy.stats as stats

    
def double_gamma(width=32, TR=1, a1=6.0, a2=12., b1=0.9, b2=0.9, c=0.35):
    """
    Returns a HRF.  Defaults are the canonical parameters.
    """
    
    x_range = np.arange(0,width,TR)    
    d1 = a1*b1
    d2 = a2*b2
    
    # Vectorized
    hrf = ((x_range / d1) ** a1 * np.exp((d1 - x_range) / b1)) - (
            c * (x_range / d2) ** a2 *np.exp((d2 - x_range) / b2))
    
    return hrf


def preturb_canonical(fraction, width, TR, prng=None):
    """
    Add scaled (by <fraction> (0-1)) white noise to a randomly selected 
    canonical double gamma HRF parameter.  Returns a dict of new HRF 
    parameters, all but the perturbed one match canonical values.  It also 
    returns a numpy RandomState() object.
    
    If a RandomState() was passed via prng it is returned, having been used for 
    sampling by this function.  If <prng> was None or a number, a RandomState() 
    was created and is (also) now returned.
    
    <width> and <TR> are not used here but are needed for HRF calculations 
    downstream.
    """

    prng = process_prng(prng)
    
    np.random.set_state(prng.get_state())
        ## Pass random state from prng to np so that
        ## stats.<> will inherit the right state.
        ## There does not seem to be a way to set random
        ## state of stats.* functions directly.
    
    params = {a1:6.0, a2:12.0, b1:0.9, b2:0.9, c:0.35}
        ## The conanoical parameters
    
    keys = params.keys()
    np.random.shuffle(keys)
    par = params[keys[0]]
    
    params[keys[0]] = stats.norm.rvs(loc=par, scale=par/(1.*fraction))
        ## Grab a random value from the normal curve
        ## with its SD reduced by 0.fraction
    
    params['width'] = width
    params['TR'] = TR
        ## Add the remaining (unpreturbed) params
    
    prng.set_state(np.random.get_state())
        ## Pass the seed state from np back to
        ## prng, then we can use prng again...
    
    return params, prng

