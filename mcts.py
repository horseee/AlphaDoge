import collections
import numpy as np
bSize = 9
from utils import *
from go import *
import math

class DummyNode(object):
    def __init__(self):
        self.parent=None
        self.child_N = collections.defaultdict(float)
        self.child_W = collections.defaultdict(float)

max_depth = bSize**2*1.4
Cpuct = 1.34

class MCTSNode(object):
    def __init__(self, status, move=None, parent=None):
        if parent==None:
            parent = DummyNode()
        self.parent = parent
        self.status = status
        self.move = move
        self.is_expanded = False
        self.child_N = np.zeros([bSize*bSize+1], dtype=np.float32)
        self.child_W = np.zeros([bSize*bSize+1], dtype=np.float32)
        self.illegal_panish = 10000*(1-self.status.get_legal_moves()).reshape((1,9*9+1))
        self.P = np.zeros([bSize*bSize+1], dtype=np.float32) # prior prob of actions
        self.child_prior = np.zeros([bSize*bSize+1], dtype=np.float32) 
        self.children = {}

    def select_child(self): # selection
        cur = self
        while True:
            #self.N+=1
            if cur.is_expanded==False: break  # reach a leaf, then selection finishes
            best_move = np.argmax(cur.child_action_score) # select the best action
            print(self.N, " select child: ", best_move)
            cur = cur.add_child(best_move) # expand
        return cur
    
    def add_child(self, coord):
        if coord not in self.children:
            new_status = self.status.copy()
            new_status.play_move( coord_flat2tuple(coord) )
            self.children[coord] = MCTSNode(new_status, coord, parent=self)
        return self.children[coord]
    
    #def revert_visits(self, up_to):
    #    self.N-=1
    #    if self.parent is None or self is up_to:
    #        return
    #    self.parent.revert_visits(up_to)
    @property
    def child_action_score(self):
        return self.child_Q * self.status.to_play + self.child_U - self.illegal_panish

    @property
    def child_Q(self):
        return self.child_W / (1+self.child_N)

    @property
    def child_U(self):
        return Cpuct* self.child_prior * math.sqrt(1+self.N) / (1+self.child_N)

    @property
    def Q(self):
        return self.W / (1+self.N)

    @property
    def N(self):
        return self.parent.child_N[self.move]
    @N.setter
    def N(self, value):
        self.parent.child_N[self.move] = value

    @property
    def W(self):
        return self.parent.child_W[self.move]
    @W.setter
    def W(self, value):
        self.parent.child_W[self.move]=value
    
    def backup_unfinished(self, move_probs, value, up_to):  # probs和value通过神经网络进行估计
        self.is_expanded = True                             # 标记展开
        self.P = self.child_prior = move_probs              # 子节点先验概率
        self.N+=1                                           # 路径访问次数加 1
        self.child_W = np.ones([bSize*bSize+1],dtype=np.float32) * value    # 设置当前状态下的价值
        if self.parent is None or self is up_to:
            return
        self.parent.backup(value, up_to)                # 更新父节点

    def backup(self, value, up_to):
        self.W+=value                               # 更新对应路径的得分
        self.N+=1                                   # 更新路径的访问次数
        if self.parent is None or self is up_to:
            return
        self.parent.backup(value, up_to)        # 递归更新父节点

    def is_done(self):
        return self.status.is_game_over() or self.status.n>max_depth
