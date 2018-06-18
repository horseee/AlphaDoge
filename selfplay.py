from strategies import MCTSPlayer
import numpy as np
from utils import *
import random, time, os, sys
from PolicyNet import PolicyNet
from scipy.io import savemat


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
        #print(move, player.root.status.to_play)
        player.play_move(move)
        if player.root.is_done():
            #print('[!] finish')
            break
    #X, p, v = player.generate_data()
    return player



if __name__=='__main__':
    self_play_round = 1000
    X = []
    p = []
    v = []
    try: os.mkdir('selfplay')
    except: pass
    
    localtime = time.asctime( time.localtime(time.time()) )
    file_name = localtime.replace(' ','-')
    for r in range(self_play_round):
        print("[!] self-play round %d"%r)
        player = play(PolicyNet())
        Xi, pi, vi = player.generate_data()
        X.extend(Xi)
        p.extend(pi)
        v.extend(vi)

    savemat('selfplay/'+file_name, {'X': X, 'p':p, 'v':v}, appendmat=False)