""" Tools to allow simfMRI experiments to be used in the Hadoop 
mapreduce-esque way. """
import numpy as np


def create_chunks(nrun, ncore):
    """ A mapper that divides <nrum> simulations into <ncore> pieces, 
    returning a list of <ncore> lists, with <nrun> integers counting up
    from 0 (starting in the first list).
    
    Note: <ncore> must evenly divide <nrun>. """
    
    if (nrun % ncore) == 0:
        return np.arange(nrun).reshape(ncore, nrun/ncore).tolist()
    else:
        raise ValueError("<ncore> must evenly divide <nrun>.")


def reduce_chunks(results_in_chunks):
    """ Reduce <results_in_chunks> (a list of results lists from a parallel
    run) to a flat list of results. """
    
    results = []
    [results.extend(chunk) for chunk in results_in_chunks]
    
    return results
