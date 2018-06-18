# -*- coding: utf-8 -*-  

import argparse
import tensorflow as tf
from model import policy_value_net
from scipy.io import loadmat
import glob
import os, sys, random
import numpy as np

def to_one_hot(p):
    if isinstance(p, int):
        one_hot = np.zeros((9*9+1))
        one_hot[p] = 1
        return one_hot
    else: 
        one_hot = np.zeros((len(p),9*9+1))
        for i in range(len(p)):
            one_hot[i,p[i]] = 1
        return one_hot


if __name__ == '__main__':

    os.environ["CUDA_VISIBLE_DEVICES"] = "2"
   
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate',type=float,default=0.0001,help='learning rate')
    parser.add_argument('--epoch',type=int,default=10,help='epoch number')
    parser.add_argument('--ckpt',type=str,default='checkpoints/model',help='epoch number')
    parser.add_argument('--batch_size',type=int,default=16,help='batch size')
    args = parser.parse_args()

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
    opt = tf.train.AdamOptimizer(args.learning_rate).minimize(loss)

    # deployment and save checkpoint
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    sess = tf.Session(config=tf_config)
    try: 
        os.mkdir('checkpoints')
    except: 
        pass 
    sess.run(tf.global_variables_initializer())
    saver =  tf.train.Saver(tf.global_variables())
    try:
        if os.path.exists('checkpoints'):
            saver.restore(sess, args.ckpt)
            print('[!] Model restored from %s'%(args.ckpt))
        else: 
            print('[!] No checkpoints!')
    except:
        print('[!] No checkpoints!')

    dataset_path = glob.glob('./data/*.mat',recursive=False)
    batch_size = args.batch_size
    for i in range(len(dataset_path)):
        data = loadmat(dataset_path[i])
        X = data['X']
        p = data['p'][0]
        v = data['v'][0]
        shuffle_idx = list(range(len(X)))
        random.shuffle(shuffle_idx)
        X = X[shuffle_idx].reshape(-1,9,9,1)
        p = p[shuffle_idx]
        v = v[shuffle_idx].reshape(-1,1)
        p_onehot = to_one_hot(p)

        #print(p_one_hot.shape)
        #brea
        c = 0
        for ep in range(args.epoch):
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
                c+=1
                mean_loss.append(cur_loss)
                mean_p.append(p_loss)
                mean_v.append(v_loss)

                if c%100==0:
                    print('epoch %d, iter %d, loss=%f (p_loss:%f, v_loss:%f)'%(ep, itr, np.mean(mean_loss),np.mean(mean_p),np.mean(mean_v)))
                    mean_loss = []
                    mean_p = []
                    mean_v = []
                    c = 0
                if c%1000==0:
                    saver.save(sess, args.ckpt)
                    print('Model saved!')
            saver.save(sess, args.ckpt)
            print('Model saved!')

