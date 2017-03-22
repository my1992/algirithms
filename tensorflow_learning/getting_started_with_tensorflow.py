import tensorflow as tf
import numpy as np


def test1():
    node1 = tf.constant(3.0, tf.float32)
    node2 = tf.constant(4.0)

    node3 = tf.add(node1, node2)

    sess = tf.Session()
    print(sess.run([node1, node2]), sess.run(node3))

    a = tf.placeholder(tf.float32)
    b = tf.placeholder(tf.float32)
    adder_node = a + b  # + provides a shortcut for tf.add(a, b)
    print(sess.run(adder_node, {a: 3, b: 4.5}))
    print(sess.run(adder_node, {a: [1, 3], b: [2, 4]}))

    add_and_triple = adder_node * 3
    print(sess.run(add_and_triple, {a: 3, b: 4.5}))

    W = tf.Variable([.3], tf.float32)
    b = tf.Variable([-.3], tf.float32)
    x = tf.placeholder(tf.float32)
    linear_model = W * x + b

    init = tf.global_variables_initializer()
    # sess.run(init)
    # print(sess.run(linear_model, {x: [1, 2, 3, 4]}))
    #
    y = tf.placeholder(tf.float32)
    squared_deltas = tf.square(linear_model - y)
    loss = tf.reduce_sum(squared_deltas)
    # print(sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))
    #
    # fix_W = tf.assign(W, [-1.])
    # fix_b = tf.assign(b, [1.])
    # sess.run([fix_W, fix_b])
    # print(sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))

    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(loss)
    sess.run(init)
    for i in range(10000):
        sess.run(train, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]})
        print(sess.run([W, b]))


def test2():
    W = tf.Variable([.3], tf.float32)
    b = tf.Variable([-.3], tf.float32)

    x = tf.placeholder(tf.float32)
    linear_model = W * x + b
    y = tf.placeholder(tf.float32)

    loss = tf.reduce_sum(tf.square(linear_model - y))

    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(loss)

    x_train = [1, 2, 3, 4]
    y_train = [0, -1, -2, -3]

    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    for i in range(1000):
        sess.run(train, {x: x_train, y: y_train})

    curr_W, curr_b, curr_loss = sess.run([W, b, loss], {x: x_train, y: y_train})
    print('W:%s b:%s loss:%s' % (curr_W, curr_b, curr_loss))


def test3():
    features = [tf.contrib.layers.real_valued_column('x', dimension=1)]

    estimator = tf.contrib.learn.LinearRegressor(feature_columns=features)

    x = np.array([1., 2., 3., 4.])
    y = np.array([0., -1., -2., -3.])
    input_fn = tf.contrib.learn.io.numpy_input_fn({'x': x}, y, batch_size=4, num_epochs=1000)

    estimator.fit(input_fn=input_fn, steps=1000)

    print(estimator.evaluate(input_fn=input_fn))


def model(features, labels, mode):
    W = tf.get_variable('W', [1], dtype=tf.float64)
    b = tf.get_variable('b', [1], dtype=tf.float64)
    y = W * features['x'] + b

    loss = tf.reduce_sum(tf.square(y - labels))

    global_step = tf.train.get_global_step()
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = tf.group(optimizer.minimize(loss), tf.assign_add(global_step, 1))

    return tf.contrib.learn.ModelFnOps(mode=mode, predictions=y, loss=loss, train_op=train)


def test4():
    estimator = tf.contrib.learn.Estimator(model_fn=model)

    x = np.array([1., 2., 3., 4.])
    y = np.array([0., -1., -2., -3.])
    input_fn = tf.contrib.learn.io.numpy_input_fn({'x': x}, y, 4, num_epochs=1000)

    estimator.fit(input_fn=input_fn, steps=1000)

    print(estimator.evaluate(input_fn=input_fn, steps=10))

if __name__ == '__main__':
    test4()