# -*- coding: utf-8 -*-  

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
        self.value = 1 if self.root.properties['RE'][0]=='W' else -1   # 白方赢为1
        #self.board = np.zeros((9,9))
        self.status = GoStatus()
        self.end=False

    def peek_next_action(self):
        return self.action_n(self.step+1)

    def action_n(self, n):  # 返回第n个落子 (row,col)
        assert n>0
        if n>=self.total: return -1
        #print(self.nodes[n].properties)
        #print(len(self.nodes[n].properties.keys()))
        if len(self.nodes[n].properties.keys())!=2: 
            return None
        else:
            return coord_sgf2tuple(self.nodes[n].properties['B' if n%2==1 else 'W'][0])

    def reset(self):        # 重置棋盘
        self.step = 0
        self.cur = self.root
        #self.board = np.zeros((9,9))
        self.status.reset()
        self.end=False

    def is_end(self):       # 判断是否结束
        return self.end

    def to_play(self):
        return self.status.to_play

    def get_status(self):        # 返回状态
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
        if len(self.cur.properties.keys())!=2: 
            coord = None
        else:
            coord = coord_sgf2tuple( self.cur.properties['B' if self.step%2==1 else 'W'][0] )
        #self.board[r,c] = player
        self.status.play_move(coord)
        #self.check_capture(r,c)
        #print(self.board)
        return self.status

# 2 white, 1 black, 0 empty
if __name__=='__main__':
    sgf_file = SGFLoader('train/2015/11/10/1.sgf')
    #print(sgf_file.to(10)) # 跳到第10个状态
    #print(sgf_file.end)    # 是否结束
    #print(sgf_file.next()) # 下一个状态
    #print(sgf_file.to(-1)) # 倒数第一个状态
    #print(sgf_file.end)    # 是否结束
    #print(sgf_file.to(2))  # 跳到第二个状态
    #print(sgf_file.to(-2)) # 跳到倒数第二个状态
    print(sgf_file.root.properties)
    #while not sgf_file.end:
    #    print(sgf_file.peek_next_action(),sgf_file.to_play())
    #    print(sgf_file.next())


    