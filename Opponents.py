import numpy as np

class RandomOppo(object):
    def __init__(self):
        pass

    def make_policy(self,status):
        r = np.random.randint(0,9)
        c = np.random.randint(0,9)
        while not status.is_move_legal((r,c)):
            r+=1
            if r==9:
                r=0
                c+=1
        return (r,c)