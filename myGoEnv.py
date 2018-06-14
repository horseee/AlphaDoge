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
        'opponent': 'AlphaDoge',
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
colormap = {
        'black': pachi_py.BLACK,
        'white': pachi_py.WHITE,
}

class myGoEnv(GoEnv):
    def __init__(self,player_color, opponent, observation_type, illegal_move_mode, board_size):
        super(myGoEnv, self).__init__(player_color, opponent, observation_type, illegal_move_mode, board_size)

    def _reset_opponent(self, board):
        pass # reset AI

    def _exec_opponent_play(self, curr_state, prev_state, prev_action):
        valid = np.argwhere(self.state.board.encode()[2]==1)
        opponent_action = toGo(* random.choice(valid))
        opponent_resigned=False
        return curr_state.act(opponent_action), opponent_resigned