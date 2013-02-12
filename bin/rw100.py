""" A top-level experimental script that run 100 iterations (on 2 cores) of 
the RW example (see simfMRI.exp_examples.RW()). """
import functools
from simfMRI.exp_examples import RW
from simfMRI.analysis.plot import hist_t_all_models
from simfMRI.runclass import Run


class RunRW100(Run):
    """ An example of a 100 iteration RW experimental Run(). """
    
    def __init__(self):
        try: 
            Run.__init__(self)
        except AttributeError: 
            pass
        
        # ----
        # An instance of simfMRI.examples.* Class (or similar) 
        # should go here.
        self.BaseClass = functools.partial(RW, behave="random")  
            ## Nornalize the signature of BaseClass with 
            ## functools.partial
            ## Expects:
            ## BaseClass(self.ntrial, TR=self.TR, ISI=self.ISI, prng=prng)
        
        # ----
        # User Globals
        self.nrun = 100
        self.TR = 2
        self.ISI = 2
        self.model_conf = "rw.ini"
        self.savedir = "testdata"
        self.ntrial = 60
        
        # --
        # Optional Globals
        self.ncore = 2
    
        # ----
        # Misc
        self.prngs = None   ## A list of RandomState() instances
                            ## setup by the go() attr


if __name__ == "__main__":
    sim = RunRW100()
    sim.go(parallel=False)
        ## Results get stored internally.

    # Writing the results to a hdf5    
    results_name = "rw{0}".format(sim.nrun)
    sim.save_results(results_name)

    # And plot all the models 
    # (each is autosaved).
    hist_t_all_models(sim.savedir, results_name+".hdf5", results_name)
    
