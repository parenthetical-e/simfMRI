""" A module process trial timing information. """
import numpy as np


def dtime(arr, durations, drop=None, drop_value=0):
    """ Repeat each element or row in <arr> by the factor
    specified in durations.
    
    <drop> allows you to create sub-trial/duration time 
    representations. It is a binary list of length duration.
    '1' mean drop that entry; 0 means keep.
    
    For example, if the next element was 2 and duration was 3
    the new represenation would be [2, 2, 2] if, that is,
    drop was None or [0, 0, 0].  
    
    However if drop was [0, 1, 0] the trial would become
    [2, 0, 2].  Likwise if drop was [1, 0, 1] trial would be
    [0, 2, 0].
        
    In the above, the drop_value was set to the default (0)
    to alters this change <drop_value>, for example
    a string '0' or a bool (False) would work just as well.

    Note: If duration for that trial is less than the length
    of drop, the rightside excess entries of drop are ignored.

    Returns a list of the duration mapped trials. """
    
    trials = arr
    dtrials = []

    if drop == None:
        # Using tuple math, repeat trial by dur
        # adding flattly to dtrials.
        [dtrials.extend([trial, ] * dur) for trial, dur in zip(
            trials, durations)]
    else:
        # As above but dropping trial entries       
        mask = np.array(drop) == 1
            ## Convert drop to a bool mask
    
        for trial, dur in zip(trials, durations):
            dtrial = np.array([trial, ] * dur)
            dtrial[mask[0:dur]] = drop_value
                ## Apply mask
                ## drop rightside excess entries in drop as dur 

            dtrials.extend(dtrial.tolist())

    return np.array(dtrials)


def add_empty(data, conditions):
    """ Collected behavioral data may not include (empty)
    jitter periods.  This function corrects for that, adding 
    zero-filled rows to data when conditions is zero. 
    
    <conditions> shouls be an integer sequence of trial events.
        '0' indicates a jitter period.  In implictly assumes 
        jitter and trial lengths are the same.
    <data> should be a list. """
    from copy import deepcopy

    # Reverse for pop.
    rdata = deepcopy(data)
    rdata.reverse()

    # Assume we want to fill with zeros
    # but change to strings if data
    # is a list of strings.
    empty = 0
    if hasattr(data[0], 'capitalize'):
        ## a standard string-like method   
        empty = '0'

    data_w_empty = []
    for cond in conditions:
        if (cond == 0) or (cond == '0'):
            data_w_empty.append(empty)
        else:
            data_w_empty.append(rdata.pop())

    return data_w_empty
