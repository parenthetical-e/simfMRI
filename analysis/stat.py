import csv
import itertools
import numpy as np
import bigstats as bs
from simfMRI.io import read_hdf, get_model_meta, get_model_names
from bigstats.hist import RHist


def create_hist_list(hdf, model, stat):
    """ Create a list of Rhist (histogram) objects for <model> and 
    <stat> in the given <hdf>. 
    
    If <stat> has only one entry (as is the case for 'aic') the list will have 
    only one entry.  If however <stat> has n entries per model (like't') 
    the list will have n-1 entries. As n matches the number of columns in
    the design matrix, the rightmost will always correspond to the dummy 
    predictor and is therefore discarded. """
    
    hist_list = [] ## A list of RHist objects.
    meta = get_model_meta(hdf, model) ## metadata for naming
    
    # A handle on the hdf data
    hdfdata = read_hdf(hdf, '/' + model + '/' + stat)   
    
    # Loop over the nodes, adding the data
    # for each to a RHist. 
    for node in hdfdata:
        # Some data will be list-like
        # so try to iterate, if that fails
        # assume the data is a single number
        try:
            for ii in range(len(node)-1):
                # Init entries in hist_list as needed
                try:
                    hist_list[ii].add(node[ii])
                except IndexError:
                    hist_list.append(RHist(name=meta['dm'][ii], decimals=2))
                    hist_list[ii].add(node[ii])
        except TypeError:
            # Assume a number so hist_list has only one
            # entry (i.e. 0).
            #
            # Init entries in hist_list as needed
            try:
                hist_list[0].add(node)
            except IndexError:
                hist_list.append(RHist(name=stat, decimals=2))
                hist_list[0].add(node)

    return hist_list


def summary(hdf, model, stat):
    """ For <model> return a very simple statistical summary (as a dict) of
     <stat> from <hdf>. """

    # Create histograms for the stats
    hist_list = create_hist_list(hdf, model, stat)
    
    # Init the summary and add 
    # stats to it
    summary = {}
    for hist in hist_list:
        summary[hist.name] = {
            "mean":hist.mean(), 
            "n":hist.n(),
            "std":hist.stdev(),
            "se":hist.se(),
            "median":hist.median()}
    
    return summary


def summary_table(hdf, model, stat, name=None):
    """ For <model> return a very simple statistical summary 
    (as a dict) of <stat> from <hdf>. 
    
    If <name> is not None, the table is written to a csv file. """
    
    # Create histograms for the stats
    hist_list = create_hist_list(hdf, model, stat)
    
    # Create the summary table,
    # and give it a header.
    summary = []
    head = ["name", "M", "SD", "SE", "MEDIAN", "N"]
    summary.append(head)
    
    # Now add the stats.
    for hist in hist_list:
        summary.append(
            [hist.name, hist.mean(), hist.stdev(),
            hist.se(), hist.median(), hist.n()]
        )
    
    # And write it?
    if name != None:
        f = open('{0}.csv'.format(name), 'w')
        csvf = csv.writer(f)
        [csvf.writerow(row) for row in summary]
        f.close()

    return summary


def above(hdf, model, stat, criterion, name=None):
    """ Return the percent area above <criterion> for <stat> from <model>
    and <hdf>. If name is not None, save the areas to a table. """
    
    # Create histograms for the stats
    hist_list = create_hist_list(hdf, model, stat)
    
    areas = {}
    for hist in hist_list:
        areas[hist.name] = hist.above(criterion)
    
    # And write it?
    if name != None:
        f = open('{0}.csv'.format(name), 'w')
        csvf = csv.writer(f)
        csvf.writerow(["condition", "area_above_{0}".format(criterion)])
        [csvf.writerow([k, v]) for k, v in areas.items()]
        f.close()
    
    return areas
    
    
def pairwise_overlaps(hdf, model, stat, name=None):
    """ In <hdf> for <model> and <stat> return the overlap between each 
    condition of <stat> in the design matrix.  If the <stat> is an omnibus
    statistic, it returns 0. 
    
    If <name> is not None, the overlaps are written out in a csv table. """
    
    # Create histograms for the stats
    hist_list = create_hist_list(hdf, model, stat)
    
    if len(hist_list) == 1:
         return {hist_list[0].h.name : 0}
    else:
        # Find all pairs (as an index into hist_list)
        combinations = itertools.combinations(range(len(hist_list)), 2)  
        
        # and find all pairwise overlaps.
        pairwisedata = {}
        for pair in combinations:
            hist1 = hist_list[pair[0]]
            hist2 = hist_list[pair[1]]
            area = hist1.overlap(hist2)
            pairwisedata[hist1.name+"_"+hist2.name] = area
        
        # Write?
        if name != None:
            f = open('{0}.csv'.format(name), 'w')
            csvf = csv.writer(f)
            csvf.writerow(["pair", "percent_overlap"])
            [csvf.writerow([k, v]) for k, v in pairwisedata.items()]
            f.close()
        
        return pairwisedata


# For testing:
if __name__ == "__main__":
#     print(summary("rw_5000_learn.hdf5", "model_030", "t"))
#     print(summary_table("rw_5000_learn.hdf5", "model_030", "t", "test"))
    # print(pairwise_overlaps("rw_5000_learn.hdf5", "model_032", "t", "test_overlap"))
    print(above("rw_5000_learn.hdf5", "model_041", "t", 2.9, "test_above"))