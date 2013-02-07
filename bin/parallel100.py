""" A top-level experimental script that run 100 iterations of 
the Simple example done *in parallel* on ncores (see 
simfMRI.examples.Simple()). """
import os
import functools
from multiprocessing import Pool
from simfMRI.examples import Simple
from simfMRI.io import write_hdf
from simfMRI.analysis.plot import hist_t
from simfMRI.mapreduce import create_chunks, reduce_chunks


def _run(name, model_conf, TR, ISI):
    """ Runs a single simulation, returning a simfMRI results object. """
    
    n = 60 ## Number of trials
    exp = Simple(n, TR, ISI)
    exp.populate_models(model_conf)
    
    return exp.run(name)


def main(names, model_conf, TR, ISI):
    """ Runs a simulation for each element of names, returning
    a results list. """
    
    return [_run(name, model_conf, TR, ISI) for name in names]


if __name__ == "__main__":
    TR = 2
    ISI = 2
    nrun = 100
    model_conf = "simple.ini"
    
    ncore = 2
    
    # Setup multi
    pool = Pool(processes=ncore)
    
    # Create chunks for multi
    run_chunks = create_chunks(nrun, ncore)
    
    # Partial function application to setup main for easy
    # mapping (and later parallelization), creating pmain.
    pmain = functools.partial(main, model_conf=model_conf, TR=TR, ISI=ISI)
    results_in_chunks = pool.map(pmain, run_chunks)
    results = reduce_chunks(results_in_chunks)
    
    print("Writing results to disk.")
    results_name = "parallel{0}".format(nrun)
    write_hdf(results, os.path.join("testdata", results_name+".hdf5"))
    
    # Make a list of the models 
    # to plot and plot them 
    print("Plotting results.")
    models = ["model_01", "model_02"]
    for mod in models:
        dataf = os.path.join("testdata", results_name+".hdf5") 
        pname = os.path.join("testdata",results_name+"_"+mod)
        hist_t(dataf, mod, pname) 
    
    