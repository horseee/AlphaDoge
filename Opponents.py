import numpy as np

class RandomOppo(object):
    def __init__(self):
        pass

    def make_policy(self,status):
        r = np.random.randint(0,9)
        c = np.random.randint(0,9)
        oldr, oldc = r, c
        while not status.is_move_legal((r,c)):
            r+=1
            if r==9:
                r=0
                c+=1
                if c==9:
                    c=0
            if r==oldr and c==oldc:
                print('pass')
                return None
        print(r,c)
        return (r,c)