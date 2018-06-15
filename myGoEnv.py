from gym.envs.board_game.go import GoEnv, GoState
from gym.envs.registration import register
import pachi_py

import numpy as np
import random
from utils import *
register(
    id='MyGoEnv-v0',
    entry_point='myGoEnv:myGoEnv',
    kwargs={
        'player_color': 'black',
        'opponent': 'random',
        'observation_type': 'image3c',
        'illegal_move_mode': 'lose',
        'board_size': 9,
    },
    # The pachi player seems not to be determistic given a fixed seed.
    # (Reproduce by running 'import gym; h = gym.make('Go9x9-v0'); h.seed(1); h.reset(); h.step(15); h.step(16); h.step(17)' a few times.)
    #
    # This is probably due to a computation time limit.
    nondeterministic=True,
)

class myGoEnv(GoEnv):
    def __init__(self,player_color, opponent, observation_type, illegal_move_mode, board_size):
        super(myGoEnv, self).__init__(player_color, opponent, observation_type, illegal_move_mode, board_size)

    #def _exec_opponent_play(self, curr_state, prev_state, prev_action):
    #    valid = np.argwhere(self.state.board.encode()[2]==1)
    #    opponent_action = toGo(* random.choice(valid))
    #    opponent_resigned=False
    #    return curr_state.act(opponent_action), opponent_resigned

    def _reset_opponent(self, board):
        if self.opponent == 'random':
            self.opponent_policy = make_random_policy(np.random)
        elif self.opponent == 'alpha_doge':
            self.opponent_policy = make_doge_policy()
            
def make_random_policy(np_random):
    def random_policy(curr_state, prev_state, prev_action):
        b = curr_state.board
        legal_coords = b.get_legal_coords(curr_state.color)
        return _coord_to_action(b, np_random.choice(legal_coords))
    return random_policy

def make_doge_policy():
    return make_random_policy(np.random)

def _coord_to_action(board, c):
    '''Converts Pachi coordinates to actions'''
    if c == pachi_py.PASS_COORD: return _pass_action(board.size)
    if c == pachi_py.RESIGN_COORD: return _resign_action(board.size)
    i, j = board.coord_to_ij(c)
    return i*board.size + j

def _pass_action(board_size):
    return board_size**2

def _resign_action(board_size):
    return board_size**2 + 1