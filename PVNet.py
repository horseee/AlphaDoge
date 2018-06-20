import numpy as np
from utils import *

import tensorflow as tf 
from model import policy_value_net
class PVNet(object):
    def __init__(self, ckpt_path=None):
        self.ckpt = ckpt_path
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(graph=tf.Graph(), config=config)
        self.initialize_graph()

    def run(self, inputs):
        with self.sess.graph.as_default():
            p, v = self.sess.run([self.policy, self.value], {self.input: inputs})
            return logits2prob(p[0]), v[0][0]

    def initialize_graph(self):
        with self.sess.graph.as_default():
            self.input = get_reference_input() # placeholder
            output = policy_value_net(self.input) # output tf tensor
            self.value = output['value']
            self.policy = output['policy']
            self.sess.run(tf.global_variables_initializer())
            if self.ckpt != None:
                self.initialize_weights(self.ckpt)
                print("Model Restored from %s"%self.ckpt)
            #else: self.sess.run(tf.global_variables_initializer())
    
    def initialize_weights(self, ckpt):
        tf.train.Saver().restore(self.sess, ckpt)
        
    def make_policy(self,curr_state, prev_state, prev_action):
        return 0, 1


bsize = 9
feature_num = 1
def get_reference_input():
    return tf.placeholder(tf.float32,
                           [None, bsize, bsize, feature_num])                      
#def model_fn(x):
#    value = tf.layers.dense(tf.layers.flatten(x), units=1)
#    probs = tf.layers.dense(tf.layers.flatten(x), units=82)
#    return {'probs': probs,'value': value}

if __name__=='__main__':
    pn = PVNet('checkpoints/model')
    policy, value = pn.run(np.zeros(shape=(1,9,9,1)))
    probs = np.exp(policy)
    probs = probs/np.sum(probs)
    print(np.argmax(probs))
    print(probs)
    print(value)