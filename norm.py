""" Routines to normalize 1d and 2d array-like objects. """
import numpy as np


def zscore(arr):
    """ Returns Z scores for the given 1 or 2d array. """

    arr = np.array(arr)
    if arr.ndim > 2:
        raise ValueError("<arr> can't have more than 2 dimensions.")

    # vectorizing....
    # x is original, y is transformed,
    # u_j is the column mean
    # s_j is the column std dev
    # do:
    # for each row (i) and column (j)
    # y_i_j = (x_i_j - u_j) / s_j
    std = arr.std(0)
    mean = arr.mean(0)
    
    return np.nan_to_num((arr - mean) / std)


def percent_change(arr):
    """ Returns percent change scores for the given 1 or 2d array. """

    arr = np.array(arr)
    if arr.ndim > 2:
        raise ValueError("<arr> can't have more than 2 dimensions.")

    # vectorizing....
    # x is original, y is transformed,
    # u is the column means
    # do:
    # for each row (i) and column (j):
    # y_i_j = 100 + ((x_i_j - u_j)/u_j) * 100
    mean = arr.mean(0)

    return np.nan_to_num(100 + (((arr - mean) / mean) * 100))
