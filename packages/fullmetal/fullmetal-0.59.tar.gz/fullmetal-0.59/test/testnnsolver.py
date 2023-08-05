from metal.layers.dense import Dense
from metal.layers.softmax import Softmax

from metal.layers.conv2D import Conv2D
from metal.layers.flatten import Flatten
from metal.losses.loss import CrossEntropy
from metal.losses.loss_functions import CrossEntropy as cp
from metal.learners.neuralnetwork import NeuralNetwork
from metal.learners.solver import Solver
from metal.initializers.optimizer_init import OptimizerInitializer, Adam
from metal.initializers.scheduler_init import SchedulerInitializer
from metal.layers.pooling import Pool2D
import numpy as np
from metal.utils.functions import to_categorical
from sklearn import datasets
import tensorflow as tf
from tensorflow import keras
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import unittest

from math import sqrt, ceil

def imgs_trans(imgs_in,size):
    factor = size/imgs_in.shape[1]
    imgs_out = ndi.zoom(imgs_in, (1, factor, factor, 1), order=2)
    print(imgs_out.shape)
    return imgs_out

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

fashion_mnist = keras.datasets.fashion_mnist

(X_trainp, y_trainp), (xt, yt) = fashion_mnist.load_data()

#X_trainp=(X_trainp - np.mean(X_trainp))/np.std(X_trainp)
#X_trainp /= X_trainp.sum(axis=1, keepdims=True)

#xt_ = (xt.reshape(-1, 28, 28, 1)/255.0).astype('float32')
X_trainm = (X_trainp.reshape(-1, 28, 28, 1)/255.0).astype('float32')
y_trainm = y_trainp
#X_train = imgs_trans(X_train,28)
y_trainm = to_categorical(y_trainm.astype("int"))


X_trainm.shape,y_trainm.shape


layer = [#Conv2D(16,(3,3),'same',stride=1,optimizer=Adam(),act_fn='relu'),
#Pool2D((2,2),stride=2,optimizer=Adam()),
#Conv2D(16,(3,3),'same',stride=1,optimizer=Adam(),act_fn='relu'),
Flatten(),
Dense(256,act_fn='relu'),
Dense(10),
Softmax()
]


X_train, X_test, y_train, y_test = train_test_split(X_trainm, y_trainm, test_size = 0.4, seed = 9)

nn = NeuralNetwork(Adam(),cp(),layers=layer,validation_data=(X_test,y_test))


small_data = {
  'X_train': X_train,
  'y_train':y_train,
  'X_val': X_test,
  'y_val': y_test,
}
ss =Solver(nn,small_data,num_epochs=10, batch_size=64,
                update_rule='Adam',
                optim_config={
                  'learning_rate': 1e-3,
                },
           #checkpoint_name='check_point_1',
                verbose=True, print_every=100)

class solvernntest(unittest.TestCase):
    def testsolvernn(self):
        nn.with_solver(small_data,num_epochs=10, batch_size=64,
                        update_rule='Adam',
                        optim_config={
                          'learning_rate': 1e-3,
                        },
                   #checkpoint_name='check_point_1',
                        verbose=True, print_every=100)
        nn.solver.train()
        truacct= [0.205, 0.843, 0.846, 0.896, 0.905, 0.866, 0.901, 0.883, 0.897, 0.911, 0.926]
        truaccv=[0.20070833333333332,0.8519166666666667,0.84875,0.865625,0.8739166666666667,0.8644583333333333,0.8785416666666667,0.8790833333333333,0.878625,0.8762083333333334,0.883]
        assert nn.solver.train_acc_history == truacct
        assert nn.solver.val_acc_history == truaccv
