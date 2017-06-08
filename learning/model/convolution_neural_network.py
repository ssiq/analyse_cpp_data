import tensorflow as tf
import numpy as np


class SimpleCNN(object):
    def __init__(self,
                 filter_size,
                 filter_number,
                 strides,
                 learning_rate,
                 sess):
        '''
        :param filter_size:
        :param filter_number:
        :param strides:
        :param learning_rate:
        :param sess:
        :type sess: tf.Session
        '''
        X = tf.placeholder(dtype=tf.float32, name='X', shape=(filter_size[0], None))
        y = tf.placeholder(dtype=tf.float32, name='y')
        filter = tf.Variable(initial_value=np.random.randn(filter_size[0],
                                                           filter_size[1],
                                                           1,
                                                           filter_number),
                             dtype=tf.float32)
        W = tf.Variable(initial_value=np.random.randn(filter_number, 1),
                        dtype=tf.float32)
        b = tf.Variable(initial_value=0.0,
                        dtype=tf.float32)
        t_X = tf.reshape(X, [1, filter_size[0], -1, 1], name='reshape_X')
        net = tf.nn.conv2d(t_X, filter, strides=strides, padding='SAME', data_format='NHWC', name='conv')
        net = tf.nn.relu(net, name='relu')
        net = tf.reduce_sum(net, axis=2)
        net = tf.reshape(net, [1, -1], name='reshape_conv_output')
        net = tf.matmul(net, W) + b
        net = tf.nn.sigmoid(net)
        loss = tf.losses.mean_squared_error(net, y)
        adam = tf.train.AdamOptimizer(learning_rate=learning_rate)
        train_op = adam.minimize(loss)
        self.X = X
        self.y = y
        self._param = {'filter': filter,
                       'W': W,
                       'b': b}
        self.train_op = train_op
        self.loss = loss
        self.sess = sess
        self.net = net

    def fit(self, X, y):
        return self.sess.run(fetches=[self.loss, self.train_op], feed_dict={self.X: X, self.y: y})[0]

    def predict(self, X):
        return self.sess.run(self.net, feed_dict={self.X: X})[0]

    @property
    def param(self):
        return {k: self.sess.run(v.value()) for k, v in self._param.items()}
