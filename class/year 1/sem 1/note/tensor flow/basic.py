import tensorflow as tf
import numpy

m = numpy.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
print(m)
t1 = tf.Variable(m, dtype=tf.int32)
print(tf.rank(t1))
print(t1.shape)