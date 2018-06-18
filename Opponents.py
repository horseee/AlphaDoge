import numpy as np
import time
import threading
from PyQt5.QtCore import *

class decisionThread(QThread):
    tuple_signal = pyqtSignal(tuple)

    def __init__(self, status):
        QThread.__init__(self)
        self.status = status

    def __del__(self):
        self.wait()
    
    def run(self):
        coord = self._make_policy()
        self.tuple_signal.emit(coord)

    def set_status(self, status):
        self.status = status

    def _make_policy(self):
        status = self.status
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
                return (-1,-1)
        print("Opponent: (%d,%d)"%(r,c))
        time.sleep(1)
        return (r,c)


class RandomOppo(object):
    def __init__(self):
        pass

    def make_policy(self, status):
        p_thread = threading.Thread(target=self._make_policy())
        p_thread.start()
        return self._make_policy(status)
    
    def _make_policy(self,status):
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
        time.sleep(1)
        return (r,c)