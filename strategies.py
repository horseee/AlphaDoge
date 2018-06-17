import go, mcts, utils
import time

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
        if two_plgit ayer_mode:
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
                print(leaf.status)
            print("%d: Searched %d times in %s seconds\n\n" % (
                    status.n, self.search_n, time.time() - start))
        return self.pick_move()

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

if __name__=='__main__':
    from PolicyNet import PolicyNet
    from go import GoStatus
    mcts_player = MCTSPlayer(PolicyNet())
    print(mcts_player.suggest_move(GoStatus()))