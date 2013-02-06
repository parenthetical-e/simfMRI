""" A top-level experimental script that run 100 iterations of 
the Simple example (see simfMRI.examples.Simple()). """
import os
from simfMRI.examples import RW
from simfMRI.io import write_hdf
from simfMRI.analysis.plot import hist_t


def main((name, TR, ISI)):
    """ Does all the work. """
    
    n = 60 
        ## Number of trials
    
    exp = RW(n, 'learn', TR, ISI)
    return exp.run(name)


if __name__ == "__main__":
    TR = 2
    ISI = 2
    nrun = 100
    
    results = map(main, zip(range(nrun), [TR, ]*nrun, [ISI, ]*nrun))
        ## zip(...) yields (name, tr, isi) per iteration

    results_name = "rw{0}".format(nrun)
    
    print("Writing results to disk.")    
    write_hdf(results, os.path.join("testdata", results_name+".hdf5"))
        
    # Make a list of the models 
    # to plot and plot them
    print("Plotting results.")
    models = ["model_01", "model_02", "model_03"]
    [hist_t(os.path.join(
            "testdata", results_name+".hdf5"), mod, 
            os.path.join("testdata",results_name+"_"+mod)) 
                for mod in models]

