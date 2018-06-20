import numpy as np
import time
import threading
from PyQt5.QtCore import *
from utils import *
import tensorflow as tf

class randomOppo(QThread):
    tuple_signal = pyqtSignal(tuple)

    def __init__(self, status=None):
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

from strategies import MCTSPlayer
from PVNet import PVNet
class AlphaDoge(QThread):
    tuple_signal = pyqtSignal(tuple)

    def __init__(self, ckpt=None,seconds_per_move=5,timed_match=False,search_n=800):
        QThread.__init__(self)
        self.player = MCTSPlayer(PVNet(ckpt),seconds_per_move=seconds_per_move,timed_match=timed_match,search_n=search_n)

    def set_status(self, status):
        self.player.set_status(status)
    
    def play_move(self, coord):
        self.player.play_move(coord)

    def reset(self):
        self.player.reset()
    
    def __del__(self):
        self.wait()
    
    def run(self):
        coord = self.player.suggest_move()
        if coord==None: coord=(-1,-1)
        self.tuple_signal.emit(coord)
