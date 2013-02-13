""" Who knows what, really.  The miscellaneous goes here."""
import numpy as np


def process_prng(prng):
    """ See if <prng> is a numpy.random.RandomState object. 
    If it is return it.  If not, try and create one by 
    RandomState(<prng>), which will work of prng was 
    None or a number. """

    # See if prng is a RandomState (and so has
    # a state to get) or create a RandomState
    # overriding prng
    try:
        prng.get_state()
    except AttributeError:
        print("Creating new RandomState(). Seed: {0}".format(prng))
        prng = np.random.RandomState(prng)
    
    return prng

