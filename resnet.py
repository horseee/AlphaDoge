import tensorflow as tf
import numpy as np

def ResNet(inputs):

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
        print(x.shape)
        return x

    x = tf.layers.batch_normalization(inputs)
    print(x.shape)

    x = tf.layers.conv2d(inputs=x, filters=filters, kernel_size=kernel_size, padding='SAME', strides=strides)
    

    for i in range(res_layer):
        x = ResBlock(x, filters, kernel_size, strides, dropout_rate)

    output_filter = 1
    x = tf.layers.conv2d(inputs=x, filters=output_filter, kernel_size=kernel_size, padding='SAME', strides=strides)
    print(x.shape)

    return x
   











