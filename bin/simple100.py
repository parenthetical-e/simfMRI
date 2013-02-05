""" A top-level experimental script that run 100 iterations of 
the Simple example (see simfMRI.examples.Simple()). """
from simfMRI.examples import Simple
from simfMRI.io import write_hdf
from simfMRI.analysis.plot import hist_t

def main((name, TR, ISI)):
    """ Does all the work. """
    
    n = 60 
        ## Number of trials
    
    exp = Simple(n, TR, ISI)
    return exp.run(name)


if __name__ == "__main__":
    TR = 2
    ISI = 2
    nrun = 100
    
    results = map(main, zip(range(nrun), [TR, ]*nrun, [ISI, ]*nrun))
        ## map(...) yields (name, tr, isi)

    results_name = "simple_{0}".format(nrun)
    
    print("Writing results to disk.")    
    write_hdf(results, results_name+".hdf5")
    
    print("Plotting results.")
    hist_t('simple_100.hdf5', 'model_01', results_name)

