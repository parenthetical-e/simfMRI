""" A top-level experimental script that run 100 iterations of 
the Simple example (see simfMRI.examples.Simple()). """
import os
import functools
from simfMRI.io import write_hdf
from simfMRI.exp_examples import Simple
from simfMRI.analysis.plot import hist_t_all_models
from simfMRI.runclass import Run


class RunSimple100(Run):
    """ An example of a 100 iteration Simple experimental Run(). """
    
    def __init__():
        Run.__init__()
        
        # ----
        # A simfMRI.examples.* Class (or similar) 
        # should go here.
        self.BaseClass = Simple
        
        # ----
        # Globals
        self.nrun = 100
        self.TR = 2
        self.ISI = 2
        self.model_conf = "simple.ini"
        self.savedir = "testdata"
        self.ncore = 2


if __name__ == "__main__":
    
    rs100 = RunSimple100()
    rs100.run(parallel=True)
    
    results_name = "simple{0}".format(nrun)
    rs100.save_results(results_name)
    
    # plot TODO broken probably
    hist_t_all_models(rs100.savedir, results_name+".hdf5", results_name)
    
