import numpy as np
from utils import *

import tensorflow as tf 

class PolicyNet(object):
    def __init__(self, ckpt_path):
        self.ckpt = ckpt_path
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(graph=tf.Graph(), config=config)

    def initialize_graph(self):
        with self.sess.graph.as_default():
            self.input = get_reference_input()
            

    def make_policy(self,curr_state, prev_state, prev_action):
        return 0, 1

    
bsize = 9
feature_num = 1
def get_reference_input():
    return tf.placeholder(tf.float32,
                           [None, bsize, bsize, feature_num],
                           name='pos_tensor')

def model_fn()