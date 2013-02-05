""" Template classes for simfMRI experiments.  To create a new experiment, 
subclass and (at minimum) manually populate:

    self.trials
    self.durations
    self.data

You might also want to override

    self.noise_f
    self.hrf
    self.hrf_params
"""
import re
import numpy as np
from copy import deepcopy
from collections import defaultdict
from scikits.statsmodels.api import GLS
import simfMRI


class Exp():
    """
    A template class for running easily parallelizable event-related fMRI
    simulations.  
    
    Note: Exp() can't be run as is.  For simple run-able experiments see 
        simfMRI.bin.examples.*
    """
    
    def __init__(self,TR=2,ISI=2):
        
        # ----
        # These need to be set during subclassing
        # and before use.
        self.trials = None
        self.durations = None
        self.data = {}
        self.data['meta'] = {}
            ## meta is for model metadata
        
        # Other needed functions you
        # might want to override
        self.noise_f = simfMRI.noise.white
        self.hrf = simfMRI.hrf.double_gamma
        self.hrf_params = {'width':32,'TR':1,'a1':6.0,'a2':12.,
                'b1':0.9,'b2':0.9,'c':0.35}
        self.hrf = simfMRI.hrf.double_gamma(**self.hrf_params)
        # ----

        # ----
        # Setup globals,
        self.TR = TR
        self.ISI = ISI        

        # --
        # and intialize the simulation's (private) 
        # data structues
        self.dm = None
        self.bold = None
        self.results = {}
        self.glm = None
            ## Where the GLM object is 
            ## stored after a fit call
        # --
        # ----
        
        # ----
        # Config:
        # --
        # Move from ISI to ITI time, if needed.
        if (self.ISI % self.TR) > 0.0:
            raise ValueError('ISI must a even multiple of the TR.')
        elif self.ISI > self.TR:
            # Use multplier to transform data and trials into units
            # of TR from their native ISI.
            mult = self.ISI/self.TR
            
            trials_copy = deepcopy(self.trials)
                ## Needed to prevent circular updates
            
            trials_mult = []
            [trials_mult.extend([t,] + [0,]*(mult-1)) for t in trials_copy]
            
            data_copy = deepcopy(self.data)
            data_mult = defaultdict(list)
            for k,vals in data_copy.items():
                [data_mult[k].extend([v,] + [0,]*(mult-1)) for v in vals]
            
            # Finally replace results with the
            # expanded version
            self.trials = trials_mult
            self.data = data_mult
    
    
    def _normalize_array(self, arr, function_name):
        """ Normalize the <arr>ay using the <function_name> 
        of one of the functions in roi.norm """

        return getattr(simfMRI.norm, function_name)(arr)


    def _orth_dm(self):
        """ Orthgonalize (by regression) each col in self.dm with respect to 
        its left neighbor. """
        
        dm = self.dm  
            ## Rename for brevity
        
        # Make sure conds and ncol dm
        # are divisors
        conds = list(set(self.trials))
        nconds = len(conds) - 1     ## Drop baseline
        ncols = dm.shape[1] - 1
        if ncols % nconds:
            raise ValueError(
                "The number of condtions and shape of the dm are incompatible.")

        # If these are the same size there is nothing to
        # orthgonalize.
        if ncols != nconds:
            orth_dm = np.zeros_like(dm)
            orth_dm[:,0] = dm[:,0]
                ## Move baseline data over

            # Use num_col_per_cond, along with nconds 
            # to find the strides we need to take along
            # the DM to orthgonalize each set of col(s) 
            # belonging to each cond.
            num_col_per_cond = ncols / nconds
            for cond in conds:
                # Skip baseline
                if cond == 0: 
                    continue
                
                left = cond
                right = cond + nconds
                
                # Rolling loop over the cols_per_cond
                # orthgonalizing as we go.
                # Note: we never use cnt directly...
                for cnt in range(num_col_per_cond-1):
                    # Orthgonalize left col to right....
                    glm = GLS( dm[:,right], dm[:,left]).fit()  ## GLS(y, x)
                    orth_dm[:,right] = glm.resid
                    orth_dm[:,left] = dm[:,left]
                   
                    # Shift indices for next iteration.
                    left = deepcopy(right)
                    right = right + nconds

            self.dm = orth_dm
        else:
            print("Nothing to orthgonalize.")
    
    
    def _convolve_hrf(self, arr):
        """
        Convolves hrf basis with a 1 or 2d (column-oriented) array.
        """
        
        # self.hrf may or may not exist yet
        if self.hrf == None:
            raise ValueError('No hrf is defined. Try self.create_hrf()?')
        
        arr = np.asarray(arr)   ## Just in case 

        # Assume 2d (or really N > 1 d), 
        # fall back to 1d.
        arr_c = np.zeros_like(arr)
        try:
            for col in range(arr.shape[1]):
                arr_c[:,col] = np.convolve(
                        arr[:,col], self.hrf)[0:arr.shape[0]]
                    ## Convolve and truncate to length
                    ## of arr
        except IndexError:
            arr_c = np.convolve(arr[:], self.hrf)[0:arr.shape[0]]
        
        return arr_c
    
    
    def create_dm(self, drop=None, convolve=True):
        """ Create a unit (boxcar-only) DM with one columns for each 
        condition in self.trials.  
        
         If <convolve> the dm is convolved with the HRF (self.hrf). """

        cond_levels = sorted(list(set(self.trials)))
            ## Find and sort conditions in trials

        # Some useful counts...
        num_conds = len(cond_levels)
        num_tr = np.sum(self.durations)

        # Map each condition in trials to a
        # 2d binary 2d array.  Each row is a trial
        # and each column is a condition.
        dm_unit = np.zeros((num_tr, num_conds))
        for col, cond in enumerate(cond_levels):
            # Create boolean array use it to 
            # populate the dm with ones... 
            # which must be in tr time.
            mask_in_tr = simfMRI.timing.dtime(
                    self.trials == cond, self.durations, drop, False)

            dm_unit[mask_in_tr,col] = 1

        self.dm = dm_unit
        
        if convolve:
            self.dm = self._convolve_hrf(self.dm)


    def create_dm_param(self, names, drop=None, box=True, 
            orth=False, convolve=True):
        """ Create a parametric design matrix based on <names> in self.data. 
        
        If <box> a univariate dm is created that fills the leftmost
        side of the dm.

        If <orth> each regressor is orthgonalized with respect to its
        left-hand neighbor (excluding the baseline).
        
        If <convolve> the dm is convolved with the HRF (self.hrf). """

        cond_levels = sorted(list(set(self.trials)))
            ## Find and sort conditions in trials
       
        # Some useful counts...
        num_names = len(names)
        num_tr = np.sum(self.durations)
        
        dm_param = None
            ## Will eventually hold the 
            ## parametric DM.

        for cond in cond_levels:
            if cond == 0:
                continue
                    ## We add the baseline 
                    ## in at the end

            # Create a temp dm to hold this
            # condition's data
            dm_temp = np.zeros((num_tr, num_names))

            mask_in_tr = simfMRI.timing.dtime(
                    self.trials == cond, self.durations, drop, False)

            # Get the named data, convert to tr time 
            # then add to the temp dm using the mask
            for col, name in enumerate(names):
                data_in_tr = simfMRI.timing.dtime(
                            self.data[name], self.durations, drop, 0)

                dm_temp[mask_in_tr,col] = data_in_tr[mask_in_tr]
                    
            # Store the temporary DM in 
            # the final DM.
            if dm_param == None:
                dm_param = dm_temp  ## reinit
            else:
                dm_param = np.hstack((dm_param, dm_temp))  ## adding

        # Create the unit DM too, then combine them.
        # defining self.dm in the process
        self.create_dm(convolve=False)
        dm_unit = self.dm.copy()
        self.dm = None  
            ## Copy and reset

        if box:
            self.dm = np.hstack((dm_unit, dm_param))
        else:
            baseline = dm_unit[:,0]
            baseline = baseline.reshape(baseline.shape[0], 1)
            self.dm = np.hstack((baseline, dm_param))
                ## If not including the boxcar,
                ## we still need the baseline model.

        # Orthgonalize the regessors?
        if orth: 
            self._orth_dm()

        # Convolve with self.hrf?
        if convolve: 
            self.dm = self._convolve_hrf(self.dm)
    
    
    def create_bold(self,arr,convolve=False):
        """ 
        The provided <arr>ay becomes a noisy bold signal. 
        
        <convolve> - if True, the dm is convolved with the HRF defined by
        self.hrf().
        """
        
        arr = np.array(arr)
        try:
            self.bold = arr.sum(1)
                ## Average by col, arr might 
                ## have been 2d, need 1d.
        except ValueError:
            self.bold = arr
            
        
        self.bold += self.noise_f(self.bold.shape[0])
        if convolve:
            self.bold = self.convolve_hrf(self.bold)
    
    
    def _reformat_model(self):
        """
        Use save_state() to store the simulation's state.
        
        This private method just extracts relevant data from the regression
        model into a dict.
        """

        tosave = {
            'beta':'params',
            't':'tvalues',
            'fvalue':'fvalue',
            'p':'pvalues',
            'r':'rsquared',
            'ci':'conf_int',
            'resid':'resid',
            'aic':'aic',
            'bic':'bic',
            'llf':'llf',
            'mse_model':'mse_model',
            'mse_resid':'mse_resid',
            'mse_total':'mse_total',
            'pretty_summary':'summary'
        }
        
        # Try to get each attr (a value in the dict above)
        # first as function (without args) then as a regular
        # attribute.  If both fail, silently move on.
        model_results = {}
        for k,v in tosave.items():
            try:
                model_results[k] = deepcopy(getattr(self.glm,v)())
            except TypeError:
                model_results[k] = deepcopy(getattr(self.glm,v))
            except AttributeError:
                continue
        
        return model_results
    
    
    def save_state(self,name):
        """
        Saves most of the state of the current simulation to results, keyed
        on <name>.  Saves greedily, trading storage space for security and
        redundancy.
        """

        tosave = {
            'TR':'TR',
            'ISI':'ISI',
            'trials':'trials',
            'data':'data',
            'dm':'dm',
            'bold':'bold'
        }
            ## This list is only for attr hung directly off
            ## of self.
        
        # Add a name to results
        self.results[name] = {}
        
        # Try to get each attr (a value in the dict above)
        # first as function (without args) then as a regular
        # attribute.  If both fail, silently move on.
        for k,v in tosave.items():
            try:
                self.results[name][k] = deepcopy(getattr(self,v)())
            except TypeError:
                self.results[name][k] = deepcopy(getattr(self,v))
            except AttributeError:
                continue
        
        # Now add the reformatted data from the current model,
        # if any.
        self.results[name].update(self._reformat_model())
    
    
    def fit(self, norm='zscore'):
        """ Calculate the regression parameters and statistics. """
        
        bold = self.bold.copy()
        dm = self.dm.copy()
        
        # Normalize both the bold and dm
        if norm != None:
            bold = self._normalize_array(bold, norm)
            dm = self._normalize_array(dm, norm)

        # Add movement regressors... if present
        try:
            dm_movement = self.data['movement']
            dm = np.vstack((dm, dm_movement))
        except KeyError:
            pass
        
        # Append a dummy predictor and run the regression
        #
        # Dummy is added at the last minute so it does not
        # interact with normalization or smoothing routines.
        dm_dummy = np.ones((dm.shape[0], dm.shape[1] + 1))
        dm_dummy[0:dm.shape[0], 0:dm.shape[1]] = dm
        
        # Truncate bold or dm_dummy if needed, and Go!
        try:
            bold = bold[0:dm_dummy.shape[0]]
            dm_dummy = dm_dummy[0:len(bold),:]
        except IndexError:
            pass

        self.glm = GLS(bold, dm_dummy).fit()
    
    
    def contrast(self, contrast):
        """ Uses the current model to statistically compare predictors 
        (t-test), returning df, t and p values.
        
        <contrast> - a 1d list of [1,0,-1] the same length as the number
            of predictors in the model (sans the dummy, which is added
            silently). """
        
        if self.glm == None:
            raise ValueError("No glm present.  Try self.fit()?")
        
        contrast = self.glm.t_test(contrast)
            ## This a thin wrapper for 
            ## statsmodels contrast() method

        return contrast.df_denom, contrast.tvalue, contrast.pvalue


    def print_model_summary(self):
        """ Prints all defined model names and their docstrings. """

        # find all self.model_N attritubes and run them.
        all_attr = dir(self)
        all_attr.sort()
        past_models = []
        model_count = 0
        for attr in all_attr:
            a_s = re.split('_', attr)
            
            # Match only model_N where N is an integer
            if len(a_s) == 2:
                if (a_s[0] == 'model') and (re.match('\A\d+\Z', a_s[1])):
                    
                    model_count += 1
                    model = attr
                        ## Rename for clarity

                    # Model name must be unique.
                    if model in past_models:
                        raise AttributeError(
                                '{0} was not unique.'.format(model))
                    past_models.append(model)

                    # Now call the model and
                    # print its info out.
                    print("{0}. {1}:".format(model_count, model))
                    try:
                        func = getattr(self, model)
                        print(func.im_func.func_doc)                    
                    except KeyError:
                        print("Data not Found.  Moving on.")
                        continue


    def run(self,code):
        """
        Run all defined models in order, returning their tabulated results.
        
        <code> - the unique batch or run code for this experiment.
        
        Models are any method of the form 'model_N' where N is an
        integer (e.g. model_2, model_1012 or model_666).  Models take no
        arguments.
        """
        
        self.results['batch_code'] = code
        
        # find all self.model_N attritubes and run them.
        all_attr = dir(self)
        all_attr.sort()
        past_models = []
        for attr in all_attr:
            a_s = re.split('_',attr)
            
            # Match only model_N where N is an integer
            if len(a_s) == 2:
                if (a_s[0] == 'model') and (re.match('\A\d+\Z',a_s[1])):
                    
                    model = attr
                        ## Rename for clarity

                    # Model name must be unique.
                    if model in past_models:
                        raise AttributeError(
                                '{0} was not unique.'.format(model))
                    past_models.append(model)

                    # Now call the model and
                    # save its results.
                    print('Fitting {0}.'.format(model))
                    try:
                        getattr(self, model)()
                    except KeyError:
                        # Missing model should just be skipped.
                        print("Data not Found.  Moving on.")
                        continue
                    
                    self.save_state(name=model)
        
        return self.results
        
