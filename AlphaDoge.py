import numpy as np


colormap = {'BLACK':1, 'WHITE':2, 'NONE': 0}
class AlphaDoge(object):
    
    def __init__(self, env, color='BLACK'):
        self.env = env
        if color=='BLACK':
            self.color=1
        else: self.color=2
    
    def make_policy(self):
        return 0, 1
    
    def find_legal_pos():
        pass
        
    