import tensorflow as tf
import numpy as np

def policy_value_net(inputs):

    kernel_size = [3, 3]
    filters = 32
    strides = 1
    dropout_rate = 0.2
    res_layer = 13

    def ResBlock(x, filters, kernel_size, strides, dropout_rate):
        short_cut = x

        x = tf.layers.batch_normalization(x)
        x = tf.nn.relu(x)
        x = tf.layers.dropout(x, rate=dropout_rate)
        x = tf.layers.conv2d(inputs=x, filters=filters, kernel_size=kernel_size, padding='SAME', strides=strides)

        x = tf.layers.batch_normalization(x)
        x = tf.nn.relu(x)
        x = tf.layers.dropout(x, rate=dropout_rate)
        x = tf.layers.conv2d(inputs=x, filters=filters, kernel_size=kernel_size, padding='SAME', strides=strides)

        x = x + short_cut
        #print(x.shape)
        return x
    with tf.variable_scope("share"):
        x = tf.layers.batch_normalization(inputs)
        #print(x.shape)
        x = tf.layers.conv2d(inputs=x, filters=filters, kernel_size=kernel_size, padding='SAME', strides=strides)
        for i in range(res_layer):
            x = ResBlock(x, filters, kernel_size, strides, dropout_rate)

    with tf.variable_scope("policy"):
        policy = tf.layers.conv2d(inputs=x, filters=2, kernel_size=1, padding='SAME', strides=1)
        policy = tf.layers.batch_normalization(policy)
        policy = tf.nn.relu(policy)
        policy = tf.layers.flatten(policy)
        policy_logits = tf.layers.dense(policy, units=9*9+1) # the last one is PASS action
        #print("Policy: %s"%policy_logits.shape)

    with tf.variable_scope("value"):
        value = tf.layers.conv2d(inputs=x, filters=1, kernel_size=1, padding='SAME', strides=1)
        value = tf.layers.batch_normalization(value)
        value = tf.nn.relu(value)
        value = tf.layers.flatten(value)
        value = tf.layers.dense(value, units=64)
        value = tf.nn.relu(value)
        value = tf.layers.dense(value, units=1)
        value_out = tf.nn.tanh(value)
        #print("Value: %s"%value_out.shape)
        

    return {'policy': policy_logits, 'value': value_out}
   











