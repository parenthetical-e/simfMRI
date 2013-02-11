""" Tools to allow simfMRI experiments to be used in the Hadoop 
mapreduce-esque way. """
import shutil
import numpy as np
from simfMRI.io import write_hdf, read_hdf


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


def write_to_tmp(name, pid, results):
    """ Save the <results> list to ./tmp/<pid> """
    
    mk_tmp(pid)

    basedir = "tmp"
    write_hdf(results, os.path.join(basedir, pid, name+".hdf5"))


def reduce_tmp_files(pid):
    """ Reduce (combine) all the seperate .hdf5 files in ./tmp/<pid> into 
    a single file (./tmp/<pid>.hdf5) then delete all .hdf5 files in that
    directory. 
    
    Note: if <pid>.hdf already exists data is appended if it is unique,
    or old data is silently overwritten. """
    
    basedir = "tmp"
    reduced = h5py.File(os.join.path(basedir, pid+".hdf5"), "a")
        ## Init

    names = sorted(os.listdir(os.join.path(basedir, pid)))
    for name in names:
        if os.path.splitext(filename)[1] == ".hdf5":
            # Open the next tmp files
            # get the paths to all its data
            # and add then to reduced.
            tmp = h5py.File(os.join.path(basedir, pid, name), "r")
            paths = []
            tmp.visit(paths.append) ## Adds all data paths in hdf
                                    ## to paths
            
            for path in paths:
                reduced[path] = tmp[path].value

    # And destroy the ./tmp/<pid> directory
    rm_tmp(pid)


def mk_tmp(pid):
    """ Make a ./tmp/<pid> subdirectory. """
    
    # Create ./tmp if needed
    basedir = "tmp"
    try:
        os.mkdir(basedir)
    except OSError:
        pass
    
    try:
        # Create ./tmp/<pid> if needed
        os.mkdir(os.join.path(basedir, pid))
    except OSError:
        pass


def rm_tmp(pid):
   """ Delete a ./tmp/<pid> subdirectory (even if it contains data). """ 
   
   basedir = "tmp"
   shutil.rmtree(os.join.path(basedir, pid))

