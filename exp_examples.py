""" Examples of how to subclass simfMRI.template.* classes. """
import numpy as np
import rl
import simfMRI
import simBehave
from simfMRI.expclass import Exp
from simBehave.trials import event_random


class Simple(Exp):
    """ Run <n> one condition experiments. Return a list of results. """
    
    def __init__(self, n, TR=2, ISI=2, prng=None):
        try: 
            Exp.__init__(self, TR=2, ISI=2, prng=None)
        except AttributeError: 
            pass
        
        self.trials = np.array([0,]*n + [1,]*n)
        self.durations = [1, ] * len(self.trials)
        
        self.prng.shuffle(self.trials)



class TwoCond(Exp):
    """
    Simulate two conditions using one then the other as the BOLD signal.
    """
    
    def __init__(self, n, TR=2, ISI=2, prng=None):
        try: 
            Exp.__init__(self, TR=2, ISI=2, prng=None)
        except AttributeError: 
            pass
        
        # event_random(N,k,mult=1)
        self.trials, self.prng = event_random(2, n, 1, self.prng)
        self.trials = np.array(self.trials)
        
        self.durations = [1, ] * len(self.trials)

  
class RW(Exp):
    """
    Generate and fit behavioral data with a Rescorla-Wagner RL model.
    Use the RPE and values from these fits to run fMRI simulations with
    parameteric regressors.
    """
    def __init__(self, n, behave='learn', TR=2, ISI=2, prng=None):
        Exp.__init__(self, TR=2, ISI=2, prng=None)

        n_cond = 1
        n_trials_cond = n
        trials = []
        acc = []
        p = []
        if behave is 'learn':
    		trials, acc, p, self.prng = simBehave.behave.learn(
    				n_cond, n_trials_cond, 3, True, self.prng)
        elif behave is 'random':
    			trials, acc, p, self.prng = simBehave.behave.random(
                        n_cond,n_trials_cond, 3, self.prng)
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
        self.data['rand'] = self.prng.rand(len(self.trials))


