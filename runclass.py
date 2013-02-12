""" A template Class for top-level experimental runs. """
import os
from numpy.random import RandomState
from multiprocessing import Pool
from simfMRI.io import write_hdf, get_model_names
from simfMRI.analysis.plot import hist_t
from simfMRI.mapreduce import create_chunks, reduce_chunks
from simfMRI.misc import process_prng


class Run():
    """ A template for an experimental run. """
    
    def __init__(self):

        # ----
        # An instance of simfMRI.examples.* Class (or similar) 
        # should go here.
        self.BaseClass = None  ##  = BaseClass()
        
        # ----
        # User Globals
        self.nrun = None
        self.TR = None
        self.ISI = None
        self.model_conf = None
        self.savedir = None
        self.ntrial = None
            
        # --
        # Optional Globals
        self.ncore = None
    
        # ----
        # Misc
        self.prngs = None   ## A list of RandomState() instances
                            ## setup by the go() attr
    
    
    def __call__(self, (names, prng)):
        return self._singleloop((names, prng))


    def _single(self, name, prng):
        """ Using the BaseClass attribute run a simulation exp named
        <name> using the given prng.  Returns a dictionary of results. """
    
        print("Experiment {0}.".format(name))
        
        exp = self.BaseClass(self.ntrial, TR=self.TR, ISI=self.ISI, prng=prng)
        exp.populate_models(self.model_conf)

        return exp.run(name)


    def _singleloop(self, (names, prng)):
        """ Loop over <names> and run an Exp for each.  Each Exp() uses
        prng, a RandomState(). Returns a list of results dictionaries. """
        
        return [self._single(name, prng) for name in names]    
            
            
    def go(self, parallel=False):
        """ Run an experimental run, results are stored the 
        results attribute. """
        
        if parallel:
            # ----
            # Setup chunks and seeds
            self.run_chunks = create_chunks(self.nrun, self.ncore)
            self.prngs = [process_prng(ii+10) for ii in range(
                    len(self.run_chunks))]
            
            # ----
            # Create a pool, and use it,
            # and store the results
            pool = Pool(self.ncore)
            results_in_chunks = pool.map(self, zip(self.run_chunks, self.prngs))
                    ## Calling self here works via __call__

            self.results = reduce_chunks(results_in_chunks)
        else:
            # Run an experimental Run, and save to
            # self.results
            self.prngs = [process_prng(42), ]
            
            self.results = self._singleloop((range(self.nrun), self.prngs[0]))
                    ## Calling self here works via __call__
    
    
    def save_results(self, name):
        """ Save results as <name> in the dir specified in the 
        savedir attribute. """

        # ----
        # Create savedir if needed
        try:
            os.mkdir(self.savedir)
        except OSError:
            pass
        
        print("Writing results to disk.")
        savepath = os.path.join(self.savedir, name+".hdf5")
        
        write_hdf(self.results, savepath)

        