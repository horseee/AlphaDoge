import go, mcts, utils
import time
import numpy as np
from utils import *
bSize = 9
class MCTSPlayer(object):
    
    def __init__(self, network,status=None, seconds_per_move=5,timed_match=False,search_n=800, two_player_mode=False):
        self.network = network
        self.seconds_per_move = seconds_per_move
        self.root = None
        self.result = 0
        self.timed_match=timed_match
        self.search_n = search_n
        if two_player_mode:
            self.temp_threshold = -1
        else:
            self.temp_threshold = (bSize**2 // 12)//2 *2
        self.initialize_game(status)

    def initialize_game(self, status=None):
        if status==None:
            status = go.GoStatus()
        self.root = mcts.MCTSNode(status)
        self.result=0
    
    def suggest_move(self, status):
        start = time.time()
        if self.timed_match:
            while time.time() - start < self.seconds_per_move:
                leaf = self.tree_search()
        else:
            cur_n = self.root.N
            while self.root.N < cur_n + self.search_n:
                leaf = self.tree_search()
                #print(leaf.status)
            print("%d: Searched %d times in %s seconds\n\n" % (
                    status.n, self.search_n, time.time() - start))
        return self.pick_move()

    def play_move(self, coord):
        self.root = self.root.add_child(coord_tuple2flat(coord))
        self.status = self.root.status
        del self.root.parent.children

    def pick_move(self):
        pick = np.argmax(self.root.child_N)
        return utils.coord_flat2tuple(pick)

    def tree_search(self):
        leaf = self.root.select_child() # selection
        if leaf.is_done():
            value = 1 if leaf.status.get_score()>0 else -1
            leaf.backup(value, self.root)     
        else:
            net_input = leaf.status.board.reshape(-1,bSize,bSize,1)
            move_probs, value = self.network.run(net_input)
            leaf.backup_unfinished(move_probs,value,self.root)
        return leaf

    def record_play(self):
        sgf_head = "(;GM[1]FF[4]CA[UTF-8]\nRU[Chinese]SZ[9]KM[7.0]TM[300]\nPW[Gnugo-3.7.10-a1]PB[CrazyStone-0002]WR[1800]BR[2693]DT[2015-12-03]PC[(CGOS) 9x9 Computer Go Server]RE[B+4.0]GN[14411]"

if __name__=='__main__':
    from PolicyNet import PolicyNet
    from go import GoStatus
    mcts_player = MCTSPlayer(PolicyNet())
    print(mcts_player.suggest_move(GoStatus()))