from strategies import MCTSPlayer
import numpy as np
from utils import *
import random, time
from PolicyNet import PolicyNet

def play(network):
    search_n = 100
    player = MCTSPlayer(network=network)

    player.initialize_game()

    while True:
        start = time.time()
        current_n = player.root.N
        while player.root.N < current_n + search_n:
            player.tree_search()
        
        move = player.pick_move()
        print(move, player.root.status.to_play)
        player.play_move(move)
        if player.root.is_done():
            print('[!] finish')
            break
    return player
        
        
        
if __name__=='__main__':
    play(PolicyNet())