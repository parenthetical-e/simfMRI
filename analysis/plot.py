import os
import numpy as np
import itertools
import matplotlib.pyplot as plt
from bigstats.hist import RHist
from simfMRI.io import read_hdf_inc, get_model_meta, get_model_names


def noise_spectrum(noise, name=None):
    """TODO"""
    
    pass


def hist_t_all_models(path, hdf, basename):
    """ Given a <path> and the <hdf> name, plot and save all the models in
    the <hdf>, prefixing each with <basename>.
    """
    
    hdfpath = os.path.join(path, hdf)
    
    # Make a list of the models 
    # to plot and plot them 
    models = get_model_names(hdfpath)
    for mod in models:
        print("Plotting {0}.".format(mod))
        
        pname = os.path.join(path, basename+"_"+mod)
        hist_t(hdfpath, mod, pname)


def hist_t(hdf,model,name=None):
    """ 
    Plot histograms of the t values in <hdf> for each condition in 
    <model>.
    
    If <name> is not None the plot is saved as <name>.pdf.
    """

    meta = get_model_meta(hdf, model)
    hist_list = []
    for dm_col in meta['dm']:
        # Make an instance RHist for the list.
        hist = RHist(name=dm_col,decimals=1)
        hist_list.append(hist)
    
    # read_hdf_inc returns a generator so....
    tdata = read_hdf_inc(hdf,'/'+ model + '/t')
    for ts in tdata:
        # get the tvals for each instance of model
        # and add them to the hist_list,
        [hist_list[ii].add(ts[ii]) for ii in range(len(ts)-1)]
            ## The last t in ts is the constant, which we 
            ## do not want to plot.

    # Create a fig, loop over the hist_list
    # plotting each on fig.axes = 0.
    fig = plt.figure()
    fig.add_subplot(111)
    colors = itertools.cycle(
                ['DarkGray', 'DarkBlue', 'DarkGreen', 'MediumSeaGreen'])
                    ## Using html colors...
    
    [h.plot(fig=fig,color=colors.next(),norm=True) for h in hist_list]
    
    # Prettify the plot
    ax = fig.axes[0]
    ax.set_xlabel('t-values')
    ax.set_ylabel('P(t)')

    # Add vetical lines representing significance tresholds
    ax.axvline(x=1.7822,label='p < 0.05',color='red',linewidth=4)
    ax.axvline(x=2.6810,label='p < 0.01',color='red',linewidth=3)
    ax.axvline(x=3.0545,label='p < 0.005',color='red',linewidth=2)
    ax.axvline(x=4.3178,label='p < 0.0005',color='red',linewidth=1)
        ## tval lines assume N=12 subjects

    plt.xlim(-10,15)
    plt.legend()
    plt.title('{0} -- BOLD: {1}'.format(model,meta['bold']))

    if name != None:
        plt.savefig(name+".pdf")
        

# FROM MASTER:
# """ A set of plotting routines for simfMRI.exp results objects"""
# import matplotlib.pyplot as plt
# import numpy as np
# import simfMRI

# frac overlap, howto calc?
# quant how?
    # mean beta w/ CI?
    # boxplot instead?
    # Asses noise effect how?

# code to do plots of hrf/raw data
# what does the corr w acc tell us
    # anything that generalizes?

# make sure unit is as it should be.  The complete lack of corr with value id odd, esp for t90

# do with td (3 state)
# do with rc

# def hist_t_delta(results,glm_name,hist_title='Data'):
    
#     glm_data = simfMRI.misc.repack_glm(results,glm_name)
#     tvalues = np.array(glm_data['t'])

#     nan_mask = np.isnan(tvalues)
#     tvalues[nan_mask] = 0.0
#         # nans break hists
    
#     plt.rcParams['font.size'] = 16
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#         # fig init
    
#     # X is 0:base,1:unit,2:values,3:rpes,4:acc,5:rand,6:dummy
#     dataloc = [4,2,3,5]
#     labels = ['Accuracy','Value','RPE','Random']
#     colors = ['orange','green','blue','black']
#     hist_params = dict(bins=100,histtype='stepfilled',alpha=0.4,normed=True)
#     for lc,lb,co in zip(dataloc,labels,colors):
#         print(lc,lb,co)
#         ax.hist(tvalues[:,lc],label=lb,color=co,**hist_params)
    
#     ax.axvline(x=2.015,label='p < 0.05',color='red',linewidth=3)
#     ax.axvline(x=3.36493,label='p < 0.01',color='red',linewidth=2)
#     ax.axvline(x=4.03214,label='p < 0.005',color='red',linewidth=1)

#     ax.set_xlabel('t-values')
#     ax.set_ylabel('Normalized counts')
#     plt.xlim(-10,15)
#     plt.ylim(0,.6)
#     plt.legend(bbox_to_anchor=(1.10, 1.10))
#     plt.title(hist_title)
#     plt.show()


# def hist_beta_delta(results,glm_name):
#     """
#     Plot a prety histogram, masking values over or under 10.
#     """
#     import numpy as np

#     glm_data = simfMRI.misc.repack_glm(results,glm_name)
#     betas = np.ma.asarray(glm_data['beta'])
#     betas = np.ma.masked_outside(betas,-10,10)
#     betas = betas.filled(0.0)

#     plt.rcParams['font.size'] = 16
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#         # fig init
    
#     # X is 0:base,1:unit,2:values,3:rpes,4:acc,5:rand,6:dummy
#     dataloc = [1,4,2,3,5]
#     labels = ['Unit','Accuracy','Value','RPE','Random']
#     colors = ['black','orange','green','blue','purple']
#     hist_params = dict(bins=100,histtype='stepfilled',alpha=0.4,normed=True)
#     for lc,lb,co in zip(dataloc,labels,colors):
#         print(lc,lb,co)
#         ax.hist(betas[:,lc],label=lb,color=co,**hist_params)
    
#     ax.set_xlabel('Beta values')
#     ax.set_ylabel('Relative counts')
#     plt.xlim(-10,10)
#     plt.ylim(0,3)
#     plt.legend(bbox_to_anchor=(1.10, 1.10))

#     plt.show()


# def mean_beta_by_glm(
#         results_list=[],glm_name='glm_acc',cols={'acc':4},n_cols=7,x_vals=[30,60,90],xlab=''):
#     """
#     Plots (and returns the values of) M and SD for select beta
#     values in glm_name for given sequence of results objects.
#     If over, the data for each col is overlayed in the 
#     same plot. Up to 4 cols are allowed
#     """
#     import numpy as np
#     from collections import defaultdict

#     if len(cols) > 5:
#         raise ValueError, 'There were more than 5 cols.'

#     ## Want the M and SD data grouped by col.keys()
#     ## where each glm's data is a element in a list
#     all_M = np.zeros((len(results_list),n_cols))
#     all_SD = np.zeros_like(all_M)
#     for ii,result in enumerate(results_list):
#         glm_data = simfMRI.misc.repack_glm(result,glm_name)
#         betas = np.ma.asarray(glm_data['beta'])
#         betas = np.ma.masked_outside(betas,-10,10)

#         all_M[ii,] = betas.mean(0)
#         all_SD[ii,] = betas.std(0)
#             # get ALL column means and std devs


#     plt.rcParams['font.size'] = 16
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#         # fig init
    
#     for name,col in cols.items():
#         ax.errorbar(x=x_vals, y=all_M[:,col], yerr=all_SD[:,col],
#                 label=name,fmt='o')
    
#     x_range = x_vals[1] - x_vals[0]
#     ax.set_xticks(range(0,max(x_vals)+x_range*2,30))
#     plt.ylabel('Avg Beta')
#     plt.xlabel(xlab)
#     plt.legend()
#     plt.show()


# def mean_t_by_glm(
#         results_list=[],glm_name='glm_acc',cols={'acc':4},n_cols=7,x_vals=[30,60,90],xlab=''):
#     """
#     Plots (and returns the values of) M and SD for select beta
#     values in glm_name for given sequence of results objects.
#     If over, the data for each col is overlayed in the 
#     same plot. Up to 4 cols are allowed
#     """
#     import numpy as np
#     from collections import defaultdict

#     if len(cols) > 5:
#         raise ValueError, 'There were more than 5 cols.'
    
#     ## Want the M and SD data grouped by col.keys()
#     ## where each glm's data is a element in a list
#     all_M = np.zeros((len(results_list),n_cols))
#     all_SD = np.zeros_like(all_M)
#     for ii,result in enumerate(results_list):
#         glm_data = simfMRI.misc.repack_glm(result,glm_name)
#         tvalues = np.array(glm_data['t'])        
#         nan_mask = np.isnan(tvalues)
#         tvalues[nan_mask] = 0.0

#         all_M[ii,] = tvalues.mean(0)
#         all_SD[ii,] = tvalues.std(0)
#             # get ALL column means and std devs


#     plt.rcParams['font.size'] = 16
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#         # fig init
    
#     for name,col in cols.items():
#         ax.errorbar(x=x_vals, y=all_M[:,col], yerr=all_SD[:,col],
#                 label=name,fmt='o')
    
#     x_range = x_vals[1] - x_vals[0]
#     ax.set_xticks(range(0,max(x_vals)+x_range*2,x_range))
#     plt.ylabel('Avg t-value')
#     plt.xlabel(xlab)
#     plt.ylim(-2,10)
#     plt.legend(bbox_to_anchor=(1.10, 1.10))
#     plt.show()

#     return all_M,all_SD