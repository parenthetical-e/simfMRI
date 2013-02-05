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
        """ BOLD: condition 1 """

        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'condition 1'
        self.data['meta']['dm'] = ('baseline', 'condition 1')

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
        self.data['meta']['bold'] = 'condition 1'
        self.data['meta']['dm'] = ('baseline','condition 1','condition 2')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,1], convolve=False)
        
        self.fit(norm='zscore')
    
    
    def model_02(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'condition 2'
        self.data['meta']['dm'] = ('baseline','condition 1','condition 2')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,2], convolve=False)
        
        self.fit(norm='zscore')
    
    
    def model_03(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'condition 1 + condition 2'
        self.data['meta']['dm'] = ('baseline','condition 1','condition 2')

        self.create_dm(drop=None, convolve=True)
        self.create_bold(self.dm[:,1:3], convolve=False)
        
        self.fit(norm='zscore')
        
  

# TODO - needs updating below!  Do not use!
class RW(Exp):
    """
    Generate and fit behavioral data with a Rescorla-Wagner RL model.
    Use the RPE and values from these fits to run fMRI simulations with
    parameteric regressors.
    """
    def __init__(self, n, behave='learn'):
        Exp.__init__(self, TR=2, ISI=2)

        n_cond = 1
        n_trials_cond = n
        trials = []; acc = []; p = []
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
        self.trials = trials
        self.data['acc'] = acc
        self.data['p'] = p
        self.data['best_logL'] = best_logL
        self.data['best_rl_pars'] = best_rl_pars
        self.data['value'] = values
        self.data['rpe'] = rpes
    
    # DEFINE ALL MODELS:
    def model_01(self):
        self.data['meta']['dm'] = ('baseline', 'condition 1')
        self.create_dm('boxcar', True)
        
        self.data['meta']['bold'] = 'condition 1'
        self.create_bold(self.dm[:,1], False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()
        
    
    def model_02(self):
        self.data['meta']['dm'] = ('baseline','condition 1','acc')
        self.create_dm('base_box_acc',True)

        self.data['meta']['bold'] = 'condition 1'
        self.create_bold(self.dm[:,1],False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()


    def model_03(self):
        self.data['meta']['dm'] = ('baseline','condition 1','value')
        self.create_dm('base_box_value',True)
        
        self.data['meta']['bold'] = 'condition 1'
        self.create_bold(self.dm[:,1],False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()

    
    def model_04(self):
        self.data['meta']['dm'] = ('baseline','condition 1','rpe')
        self.create_dm('base_box_rpe',True)

        self.data['meta']['bold'] = 'condition 1'
        self.create_bold(self.dm[:,1],False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()


    def model_05(self):
        self.data['meta']['dm'] = ('baseline','condition 1','rand')
        self.create_dm('base_box_rand',True)

        self.data['meta']['bold'] = 'condition 1'
        self.create_bold(self.dm[:,1],False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()


    def model_06(self):        
        self.data['meta']['dm'] = ('baseline','condition 1','value')
        self.create_dm('base_box_value',True)
        
        self.data['meta']['bold'] = 'acc'
        self.create_bold(self.convolve_hrf(self.data['acc']),False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()


    def model_07(self):
        self.data['meta']['dm'] = ('baseline','condition 1','rpe')
        self.create_dm('base_box_rpe',True)
        
        self.data['meta']['bold'] = 'acc'
        self.create_bold(self.convolve_hrf(self.data['acc']),False)
    
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
    
        self.fit()
    
    
    def model_08(self):
        self.data['meta']['dm'] = ('baseline','condition 1','rand')
        self.create_dm('base_box_rand',True)
        
        self.data['meta']['bold'] = 'acc'
        self.create_bold(self.convolve_hrf(self.data['acc']),False)
    
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
    
        self.fit()
    
    
    def model_09(self):
        self.data['meta']['dm'] = ('baseline','condition 1','rpe')
        self.create_dm('base_box_rpe',True)
        
        self.data['meta']['bold'] = 'value'
        self.create_bold(self.convolve_hrf(self.data['value']),False)
    
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
    
        self.fit()
    

    def model_091(self):
        self.data['meta']['dm'] = ('baseline','condition 1','value')
        self.create_dm('base_box_value',True)
        
        self.data['meta']['bold'] = 'value'
        self.create_bold(self.convolve_hrf(self.data['value']),False)
    
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
    
        self.fit()


    def model_10(self):
        self.data['meta']['dm'] = ('baseline','condition 1','value')
        self.create_dm('base_box_value',True)
        
        self.data['meta']['bold'] = 'rpe'
        self.create_bold(self.convolve_hrf(self.data['rpe']),False)
    
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
    
        self.fit()
    

    def model_101(self):
        self.data['meta']['dm'] = ('baseline','condition 1','rpe')
        self.create_dm('base_box_rpe',True)
        
        self.data['meta']['bold'] = 'rpe'
        self.create_bold(self.convolve_hrf(self.data['rpe']),False)
    
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
    
        self.fit()


    def model_11(self):
        self.data['meta']['dm'] = ('baseline','condition 1','acc')
        self.create_dm('base_box_acc',True)
        
        self.data['meta']['bold'] = 'rand'
        randarr = np.zeros(len(self.trials))
        for ii,t in enumerate(self.trials):
            if t >= 1: 
                randarr[ii] = np.random.rand(1)
        
        # print (np.array(self.trials) > 0.0) == (randarr > 0.0)
                
        self.create_bold(self.convolve_hrf(randarr),False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()


    def model_12(self):
        self.data['meta']['dm'] = ('baseline','condition 1','value')
        self.create_dm('base_box_value',True)

        self.data['meta']['bold'] = 'rand'
        randarr = np.zeros(len(self.trials))
        for ii,t in enumerate(self.trials):
            if t >= 1: 
                randarr[ii] = np.random.rand(1)

        # print (np.array(self.trials) > 0.0) == (randarr > 0.0)

        self.create_bold(self.convolve_hrf(randarr),False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()


    def model_13(self):
        self.data['meta']['dm'] = ('baseline','condition 1','rpe')
        self.create_dm('base_box_rpe',True)

        self.data['meta']['bold'] = 'rand'
        randarr = np.zeros(len(self.trials))
        for ii,t in enumerate(self.trials):
            if t >= 1: 
                randarr[ii] = np.random.rand(1)

        # print (np.array(self.trials) > 0.0) == (randarr > 0.0)

        self.create_bold(self.convolve_hrf(randarr),False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()


# # 2 conditiom, 60 trial per condition
# if behave is 'random':
#     trials,acc,p = simBehave.behave.random(2,n,True)
#     self.trials = trials
# elif behave is 'learn':
#     trials,acc,p = simBehave.behave.learn(2,n,3,True)
#     self.trials = trials
# else:
#     raise ValueError('behave was unknown; try random or learn.')