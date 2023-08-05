from metal.layers.dense import Dense
from metal.layers.softmax import Softmax

from metal.layers.conv2D import Conv2D
from metal.layers.flatten import Flatten
from metal.losses.loss import CrossEntropy
from metal.losses.loss_functions import CrossEntropy as cp
from metal.nn.neuralnetwork import NeuralNetwork
from metal.initializers.optimizer_init import OptimizerInitializer, Adam
from metal.initializers.scheduler_init import SchedulerInitializer
from metal.layers.pooling import Pool2D
import numpy as np
from metal.utils.functions import to_categorical
from sklearn import datasets
import tensorflow as tf
from tensorflow import keras
import scipy.ndimage as ndi
import unittest


def train_test_split(X, y, test_size=0.5, shuffle=True, seed=None):
    """ Split the data into train and test sets """
    if shuffle:
        X, y = shuffle_data(X, y, seed)
    # Split the training data from test data in the ratio specified in
    # test_size
    split_i = len(y) - int(len(y) // (1 / test_size))
    X_train, X_test = X[:split_i], X[split_i:]
    y_train, y_test = y[:split_i], y[split_i:]

    return X_train, X_test, y_train, y_test

def shuffle_data(X, y, seed=None):
    """ Random shuffle of the samples in X and y """
    if seed:
        np.random.seed(seed)
    idx = np.arange(X.shape[0])
    np.random.shuffle(idx)
    return X[idx], y[idx]


#optimizer = Adam()
data = datasets.load_digits()
X = (data.data.reshape(-1, 8, 8, 1)/255.0).astype('float32')
y = data.target
#loss = CrossEntropy
# Covnet to  one-hot encoding
y = to_categorical(y.astype("int"))
#X = imgs_trans(X,28)


layer = [Conv2D(3,(3,3),'same',stride=1,optimizer=Adam(),act_fn='relu'),
Conv2D(3,(3,3),'same',stride=1,optimizer=Adam(),act_fn='relu'),
Flatten(optimizer=Adam()),
Dense(256,optimizer=Adam(),act_fn='relu'),
Dense(10,optimizer=Adam()),
Softmax(optimizer=Adam())
]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, seed = 1)


class nnstest(unittest.TestCase):
    def testnn(self):
        nn = NeuralNetwork(Adam(),cp(),layers=layer,validation_data=(X_test,y_test))
        train_err, val_err = nn.fit(X_train, y_train, n_epochs=10, batch_size=64)
        acc = nn.eval(X_test, y_test)
        assert(acc== 0.9178272980501393)
        assert(len(layer)==len(nn.layers))
