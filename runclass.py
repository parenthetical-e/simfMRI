""" A template Class for top-level experimental runs. """
import os 
from numpy.random import RandomState
from multiprocessing import Pool
from simfMRI.io import write_hdf, get_model_names
from simfMRI.analysis.plot import hist_t
from simfMRI.mapreduce import create_chunks, reduce_chunks

# work out prng stuff it is broken!
class Run():
    """ A template for an experimental run. """
    def __init__(self):

        # ----
        # An instance of simfMRI.examples.* Class (or similar) 
        # should go here.
        self.BaseClass = None  ##  = BaseClass()
        
        # ----
        # Globals
        self.nrun = None
        self.TR = None
        self.ISI = None
        self.model_conf = None
        self.savedir = None
        self.ncore = None
        self.rwtype = None

        # ----
        # Hard coded trial count
        self.ntrial = 60
    

    def _step(self, (name, prng)):
        """ Using the BaseClass attribute run a simulation exp, 
        one step in the Run(). Returns a dictionary of results. """
    
        exp = self.BaseClass(self.ntrial, TR=self.TR, ISI=self.ISI, prng=prng)
        exp.populate_models(self.model_conf)

        return self.exp.run(name)

        
    def run(self, parallel=False):
        """ Run an experimental run, results are stored the 
        results attribute. """
        
        if parallel:
            # ----
            # Setup chunks and seeds
            self.run_chunk = create_chunks(self.nrun, self.ncore)
            self.prngs = [RandomState(ii+10) for ii in range(
                    len(self.run_chunks))]
            
            # ----
            # Create a pool, and use it,
            # and store the results
            pool = Pool(self.ncore)
            
            results_in_chunks = pool.map(self._step, 
                    zip(self.run_chunks, self.prngs))
            
            self.results = reduce_chunks(results_in_chunks)
        else:
            # Run an experimental Run, and save to
            # self.results
            self.prngs = [RandomState(42), ]
            self.results = [_step((ii, self.prngs[0])) for ii in range(
                    self.nrun))]
    
    
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

        