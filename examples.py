""" Examples of how to subclass simfMRI.template.* classes. """
import numpy as np
import rl
import simfMRI
import simBehave
from simfMRI.template import Exp
from simBehave.trials import event_random


class Simple(Exp):
    """ Run <n> one condition experiments. Return a list of results. """
    def __init__(self, n, TR=2, ISI=2):
        try: 
            Exp.__init__(self, TR=2, ISI=2)
        except AttributeError: 
            pass
        
        self.trials = np.array([0,]*n + [1,]*n)
        self.durations = [1, ] * len(self.trials)
        
        np.random.shuffle(self.trials)
    
    
    def model_01(self):
        """ BOLD: box """

        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'box'
        self.data['meta']['dm'] = ('baseline', 'box')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,1], convolve=False)

        self.fit(norm='zscore')


class TwoCond(Exp):
    """
    Simulate two conditions using one then the other as the BOLD signal.
    """
    def __init__(self, n, TR=2, ISI=2):
        try: 
            Exp.__init__(self, TR=2, ISI=2)
        except AttributeError: 
            pass
        
        # event_random(N,k,mult=1)
        self.trials = np.array(event_random(2, n, 1))
        self.durations = [1, ] * len(self.trials)

    
    def model_01(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'box1'
        self.data['meta']['dm'] = ('baseline','box1','box2')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,1], convolve=False)
        
        self.fit(norm='zscore')
    
    
    def model_02(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'box2'
        self.data['meta']['dm'] = ('baseline','box','box2')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,2], convolve=False)
        
        self.fit(norm='zscore')
    
    
    def model_03(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'box1 + box2'
        self.data['meta']['dm'] = ('baseline','box1','box2')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,1:3], convolve=False)
        
        self.fit(norm='zscore')
        
  
class RW(Exp):
    """
    Generate and fit behavioral data with a Rescorla-Wagner RL model.
    Use the RPE and values from these fits to run fMRI simulations with
    parameteric regressors.
    """
    def __init__(self, n, behave='learn', TR=2, ISI=2):
        Exp.__init__(self, TR=2, ISI=2)

        n_cond = 1
        n_trials_cond = n
        trials = []
        acc = []
        p = []
        if behave is 'learn':
    		trials, acc, p = simBehave.behave.learn(
    				n_cond, n_trials_cond, 3, True)
        elif behave is 'random':
    			trials,acc,p = simBehave.behave.random(
                        n_cond,n_trials_cond,3,True)
        else:
            raise ValueError(
                    '{0} is not known.  Try learn or random.'.format(behave))
        
        # Find best RL learning parameters for the behavoiral data
        # then generate the final data and unpack it into a list.
        best_rl_pars, best_logL = rl.fit.ml_delta(acc, trials, 0.05)
        v_dict, rpe_dict = rl.reinforce.b_delta(acc, trials, best_rl_pars[0])
        values = rl.misc.unpack(v_dict, trials)
        rpes = rl.misc.unpack(rpe_dict, trials)
        
        # Store the results in appropriate places
        self.trials = np.array(trials)
        self.durations = np.array([1, ] * len(self.trials))
        self.data['acc'] = acc
        self.data['p'] = p
        self.data['best_logL'] = best_logL
        self.data['best_rl_pars'] = best_rl_pars
        self.data['value'] = values
        self.data['rpe'] = rpes


    def model_01(self):
        """ BOLD: box """

        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'box'
        self.data['meta']['dm'] = ('baseline', 'box')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,1], convolve=False)

        self.fit(norm='zscore')
        
    
    def model_02(self):
        """ BOLD: acc, DM: ['acc', 'rpe'], orth: True. """
        
        # Create the dm.
        data_to_use = ['acc', 'rpe']
        self.data['meta']['dm'] = ['box',] + data_to_use
        self.create_dm_param(names=data_to_use, box=True, orth=True,
                convolve=True)

        # Create the bold.
        # Lookup the index of bold_name in data_to_use
        # then offest by 1 to account for the boxcar
        bold_name = 'acc'
        self.data['meta']['bold'] = bold_name        
        boldarr = self.dm[:,data_to_use.index(bold_name)+1]
        self.create_bold(boldarr, convolve=False)

        # And fit
        self.fit(norm='zscore')


    def model_03(self):
        """ BOLD: acc, DM: ['acc', 'value'], orth: True. """
        
        # Create the dm.
        data_to_use = ['acc', 'value']
        self.data['meta']['dm'] = ['box',] + data_to_use
        self.create_dm_param(names=data_to_use, box=True, orth=True,
                convolve=True)

        # Create the bold.
        # Lookup the index of bold_name in data_to_use
        # then offest by 1 to account for the boxcar
        bold_name = 'acc'
        self.data['meta']['bold'] = bold_name        
        boldarr = self.dm[:,data_to_use.index(bold_name)+1]
        self.create_bold(boldarr, convolve=False)

        # And fit
        self.fit(norm='zscore')
