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
        self.nodes = self.sgf.children[0].nodes   # 保存了所有落子的记录
        self.root = self.sgf.children[0].root     # 状态节点（编号0） 
        self.total = len(self.nodes)              # 总的状态数
        self.step = 0                             # 目前是第step步                  
        self.cur = self.root                      # 当前所处的树节点
        #self.board = np.zeros((9,9))
        self.status = GoStatus()
        self.end=False

    def action_n(self, n):  # 返回第n个落子 (row,col)
        assert n>0
        if n>self.total: return None
        return coord_sgf2tuple(self.nodes[n].properties['B' if n%2==1 else 'W'][0])

    def reset(self):        # 重置棋盘
        self.step = 0
        self.cur = self.root
        #self.board = np.zeros((9,9))
        self.status.reset()
        self.end=False

    def is_end(self):       # 判断是否结束
        return self.end

    def state(self):        # 返回状态
        return self.status

    def next(self):         # 进入下一个状态
        return self._next()
    
    def to(self, n):        # 直接到达状态n （0为空棋盘）
        return self._to(n)
    
    def __getitem__(self, key): # sgf[2] 表示返回第2个落子
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
        r, c = coord_sgf2tuple( self.cur.properties['B' if self.step%2==1 else 'W'][0] )
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


    