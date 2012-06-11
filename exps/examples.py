import simfMRI
import numpy as np
from simfMRI.template import Exp

class Simple(Exp):
    """ Run <n> one condition experiments. Return a list of results. """
    def __init__(self,n):
        try: Exp.__init__(self)
        except AttributeError: pass
        
        self.trials = np.array([0,]*n + [1,]*n)
        np.random.shuffle(self.trials)
    
    
    def model_01(self):
        """ BOLD: condition 1 """
        from simfMRI.dm import construct

        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'condition 1'
        self.data['meta']['dm'] = ('baseline','condition 1')

        self.create_dm('boxcar',True)
        self.create_bold(self.dm[:,1],False)

        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)

        self.fit()
    

class TwoCond(Exp):
    """
    Simulate two conditions using one then the other as the BOLD signal.
    """
    def __init__(self,n):
        try: Exp.__init__(self)
        except AttributeError: pass
        from simBehave.trials import event_random
        
        # event_random(N,k,mult=1)
        self.trials = event_random(2,60,1)
            ## 2 cond (+1 baseline), 60 trials per.

    
    def model_01(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'condition 1'
        self.data['meta']['dm'] = ('baseline','condition 1','condition 2')

        self.create_dm('boxcar',True)
        self.create_bold(self.dm[:,1])
        
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
        
        self.fit()
    
    
    def model_02(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'condition 2'
        self.data['meta']['dm'] = ('baseline','condition 1','condition 2')

        self.create_dm('boxcar',True)
        self.create_bold(self.dm[:,2])
        
        self.dm = self.normalize_f(self.dm)
        self.bold = self.normalize_f(self.bold)
        
        self.fit()
    
    
    def model_03(self):
        # Add some meta data describing the model...
        self.data['meta']['bold'] = 'condition 1 + condition 2'
        self.data['meta']['dm'] = ('baseline','condition 1','condition 2')

        self.create_dm('boxcar',True)
        self.create_bold(self.dm[:,1:3])
        
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