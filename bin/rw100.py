""" A top-level experimental script that run 100 iterations of 
the Simple example (see simfMRI.examples.Simple()). """
import os
from functools import partial
from simfMRI.examples import RW
from simfMRI.io import write_hdf
from simfMRI.analysis.plot import hist_t


def main(name, model_conf, TR, ISI):
    """ Does all the work. """
    
    n = 60 ## Number of trials
    exp = RW(n, 'learn', TR, ISI)
    exp.populate_models(model_conf)

    return exp.run(name)


if __name__ == "__main__":
    TR = 2
    ISI = 2
    nrun = 1
    model_conf = "rw.ini"
    
    # Partial function application to setup main for easy
    # mapping (and later parallelization), creating pmain.
    pmain = partial(main, model_conf=model_conf, TR=TR, ISI=ISI)
    results = map(pmain, range(nrun))
    
    results_name = "rw{0}".format(nrun)
    
    print("Writing results to disk.")    
    write_hdf(results, os.path.join("testdata", results_name+".hdf5"))
    
    # Make a list of the models 
    # to plot and plot them 
    print("Plotting results.")
    models = ["model_01", "model_02", "model_03"]
    for mod in models:
        dataf = os.path.join("testdata", results_name+".hdf5") 
        pname = os.path.join("testdata",results_name+"_"+mod)
        hist_t(dataf, mod, pname) 
    
    

