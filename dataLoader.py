import os, sys 
import sgf
import numpy as np
from utils import *
from go import *
from copy import copy

class SGFLoader(object):
    """ Loader for single sgf files
    """
    def __init__(self, filepath):
        self.open(filepath)

    def open(self, filename):
        self.filepath = filename
        with open(filename, 'rt') as f:
            self.sgf = sgf.parse(f.read())
        self.nodes = self.sgf.children[0].nodes
        self.root = self.sgf.children[0].root
        self.total = len(self.nodes)
        self.step = 0
        self.cur = self.root 
        #self.board = np.zeros((9,9))
        self.status = GoStatus()
        self.end=False

    def action_n(self, n):
        assert n>0
        if n>self.total: return None, None
        return coord_sgf2doge(self.nodes[n].properties['B' if n%2==1 else 'W'][0])

    def reset(self):
        self.step = 0
        self.cur = self.root
        #self.board = np.zeros((9,9))
        self.status.reset()
        self.end=False

    def is_end(self):
        return self.end

    def state(self):
        return self.status

    def next(self):
        return self._next()
    
    def to(self, n):
        return self._to(n)
    
    def __getitem__(self, key):
        return self.action_n(key)

    def _to(self, n):
        if n<0: n = self.total-n+1 # the last
        assert n>=0
        if self.step>n: self.reset()

        while self.step < n and self.end==False:
            self.next()
        return self.status

    def _next(self):
        if self.cur.next==None:
            #print("End!")
            self.end = True
            return self.status

        self.cur = self.cur.next
        self.step+=1
        player = colormap['black'] if self.step%2==1 else colormap['white']
        r, c = coord_sgf2doge( self.cur.properties['B' if self.step%2==1 else 'W'][0] )
        if r!=None:
            #self.board[r,c] = player
            self.status.play_move((r,c))
            #self.check_capture(r,c)
        #print(self.board)
        return self.status

# 2 white, 1 black, 0 empty
if __name__=='__main__':
    sgf_file = SGFLoader('train/2015/11/10/1.sgf')
    print(sgf_file.to(10))
    print(sgf_file.end)
    print(sgf_file.next())
    print(sgf_file.to(-1))
    print(sgf_file.end)
    print(sgf_file.to(2))
    print(sgf_file.to(-2))


    