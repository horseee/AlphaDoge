from strategies import MCTSPlayer
import numpy as np
from utils import *
import random, time, os, sys
from PVNet import PVNet
from model import policy_value_net
from scipy.io import savemat
import tensorflow as tf

seconds_per_move=5
timed_match=False
search_n=800
ckpt = 'checkpoints/model'
learning_rate = 0.0001
self_play_round = 100
batch_size = 10
from utils import to_one_hot

def play(network):
    search_n = 100
    player = MCTSPlayer(network=network,seconds_per_move=seconds_per_move,timed_match=timed_match,search_n=search_n, player_mode=0)
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
    X = []
    p = []
    v = []
    try: os.mkdir('selfplay')
    except: pass
    rl_ckpt = 'selfplay/checkpoints/model'
    

    g_train = tf.Graph()
    with g_train.as_default():
        data_input = tf.placeholder(dtype='float32',shape=(None, 9, 9, 1))
        p_input = tf.placeholder(dtype='float', shape=(None, 9*9+1)) #考虑PASS
        v_input = tf.placeholder(dtype='float', shape=(None, 1)) #考虑PASS
        # load model
        net_out = policy_value_net(data_input)
        policy_logits = net_out['policy']
        value_out = net_out['value']
        policy_loss = tf.losses.softmax_cross_entropy(p_input, policy_logits)
        value_loss = tf.losses.mean_squared_error(v_input, value_out)
        loss = policy_loss+value_loss
        opt = tf.train.AdamOptimizer(learning_rate).minimize(loss)

        # deployment and save checkpoint
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        sess = tf.Session(config=tf_config)

        sess.run(tf.global_variables_initializer())
        saver =  tf.train.Saver(tf.global_variables())
        try:
            if os.path.exists('selfplay/checkpoints'):
                saver.restore(sess, rl_ckpt)
                print('[!] Model restored from %s'%(rl_ckpt))
            else: 
                print('[!] No checkpoints!')
        except:
            print('[!] No checkpoints!')



    localtime = time.asctime( time.localtime(time.time()) )
    file_name = localtime.replace(' ','-')
    mean_loss = []
    mean_p = []
    mean_v = []

    for r in range(self_play_round):
        g_play = tf.Graph()
        with g_play.as_default():
            print("[!] self-play round %d"%r)
            player = play(PVNet(rl_ckpt))
            Xi, pi, vi = player.generate_data()
            X.extend(Xi)
            p.extend(pi)
            v.extend(vi)
    X = np.array(X)
    p = np.array(p)
    v = np.array(v)

    #savemat('selfplay/'+file_name, {'X': X, 'p':p, 'v':v}, appendmat=False)
    shuffle_idx = list(range(len(X)))
    random.shuffle(shuffle_idx)
    X = X[shuffle_idx].reshape(-1,9,9,1)
    p = p[shuffle_idx]
    v = v[shuffle_idx].reshape(-1,1)
    p_onehot = to_one_hot(p)
    c = 0
    with g_train.as_default():
        print('----- training -----')
        mean_loss = []
        mean_p = []
        mean_v = []
        for itr in range(0,len(X),batch_size):
            # prepare data bactch
            if itr+batch_size>=len(X):
                cat_n = itr+batch_size-len(X)
                cat_idx = random.sample(range(len(X)),cat_n)

                batch_X = np.concatenate((X[itr:],X[cat_idx]),axis=0)
                batch_p = np.concatenate((p_onehot[itr:],p_onehot[cat_idx]),axis=0)
                batch_v = np.concatenate((v[itr:],v[cat_idx]),axis=0)
            else:
                batch_X = X[itr:itr+batch_size]        
                batch_p = p_onehot[itr:itr+batch_size]
                batch_v = v[itr:itr+batch_size]

            _, cur_loss, p_loss, v_loss = sess.run([opt, loss, policy_loss, value_loss], {data_input: batch_X, p_input: batch_p, v_input: batch_v})
            
            mean_loss.append(cur_loss)
            mean_p.append(p_loss)
            mean_v.append(v_loss)

            if c%100==0:
                print('iter %d, loss=%f (p_loss:%f, v_loss:%f)'%(itr, np.mean(mean_loss),np.mean(mean_p),np.mean(mean_v)))
                mean_loss = []
                mean_p = []
                mean_v = []
                c = 0
                saver.save(sess, rl_ckpt)
                    
        saver.save(sess, rl_ckpt)
    #