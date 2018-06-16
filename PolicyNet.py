import numpy as np
from utils import *

import tensorflow as tf 

class PolicyNet(object):
    def __init__(self, ckpt_path=None):
        self.ckpt = ckpt_path
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(graph=tf.Graph(), config=config)
        self.initialize_graph()

    def run(self, inputs):
        return self.sess.run([self.output], {self.input: inputs})
    
    def initialize_graph(self):
        with self.sess.graph.as_default():
            self.input = get_reference_input() # placeholder
            self.output = model_fn(self.input) # output tf tensor
            if self.ckpt != None:
                self.initialize_weights(self.ckpt)
            else: self.sess.run(tf.global_variables_initializer())
    
    def initialize_weights(self, ckpt):
        tf.train.Saver().restore(self.sess, ckpt)
        
    def make_policy(self,curr_state, prev_state, prev_action):
        return 0, 1

bsize = 9
feature_num = 1
def get_reference_input():
    return tf.placeholder(tf.float32,
                           [None, bsize, bsize, feature_num],
                           name='pos_tensor')                      
def model_fn(x):
    return tf.layers.conv2d(x, filters=64, kernel_size=3, strides=1, padding='SAME')

if __name__=='__main__':
    pn = PolicyNet()
    out = pn.run(np.ones(shape=(1,9,9,1)))
    print(out)