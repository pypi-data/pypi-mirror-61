import cupy as cp
from autogradgpu.tensor import Tensor
from autogradgpu.parameter import Parameter
from metalgpu.module import Module
from autogradgpu.dependency import Dependency
import math
import copy
from metalgpu.layers.layer import Layer
from metalgpu.utils.layer_data_manipulations import *

class Dense(Layer):
    __slots__ =( 'layer_input','n_units','trainable', 'w','b', 'seed','type' )
    """A fully-connected NN layer.
    Parameters:
    -----------
    n_units: int
        The number of neurons in the layer.
    input_shape: tuple
        The expected input shape of the layer. For dense layers a single digit specifying
        the number of features of the input. Must be specified if it is the first layer in
        the network.
    example shape:
        w = cp.random.randn(6,5)
        i = cp.random.randn(2,6)
        cp.dot(i,w) + cp.random.randn(1,5)
    """

    def __init__(self, n_units, input_shape=None, seed=None):
        self.layer_input = None
        self.input_shape = input_shape
        self.n_units = n_units
        self.trainable = True
        self.w = None
        self.b = None
        self.seed = seed
        self.load_params_ = False

    def load_params(self, weights, bias, trainable = False):
        self.load_params_ = True
        self.trainable = trainable
        if self.trainable == False:
            self.w = Parameter(data = weights,requires_grad=False)
            self.b = Parameter(data = bias.reshape(-1,1),requires_grad=False)
        elif self.trainable == True:
            self.w = Parameter(data = weights)
            self.b = Parameter(data = bias.reshape(-1,1))


    def load_optimzer(self,optimizer=None):
        # Weight optimizers
        if optimizer is not None:
            self.w_opt  = copy.copy(optimizer)
            self.b_opt = copy.copy(optimizer)

    def initialize(self, optimizer=None):
        cp.random.seed(self.seed)
        # Initialize the weights
        limit = 1 / math.sqrt(self.input_shape[0])

        if self.trainable == False:
            self.w = Parameter(data = cp.random.uniform(-limit, limit, (self.input_shape[0], self.n_units)), requires_grad=False)
            self.b = Parameter(data = cp.zeros((1, self.n_units)),requires_grad=False)
        elif self.trainable == True:
            self.w = Parameter(data = cp.random.uniform(-limit, limit, (self.input_shape[0], self.n_units)))
            self.b = Parameter(data = cp.zeros((1, self.n_units)))
        # Weight optimizers
        if optimizer is not None:
            self.w_opt  = copy.copy(optimizer)
            self.b_opt = copy.copy(optimizer)

    def parameters_(self):
        return np.prod(self.W.shape) + np.prod(self.b.shape)

    def forward_pass(self, x, training=True):
        self.layer_input = x.data
        self.type = type(x)
        depends_on: List[Dependency] = []

        data = x.data.dot(self.w.data) + self.b.data
        requires_grad = x.requires_grad or self.w.requires_grad or self.b.requires_grad
        if training:
            if requires_grad:
                if self.w.requires_grad:
                    depends_on.append(Dependency(self.w, self.grad_w_dense))
                if self.b.requires_grad:
                    depends_on.append(Dependency(self.b, self.grad_b_dense))
                if x.requires_grad:
                    depends_on.append(Dependency(x, self.grad_a_dense))
            else:
                depends_on = []
        return self.type(data=data,requires_grad=requires_grad,depends_on=depends_on)


    def grad_w_dense(self, accum_grad):
        # Calculate gradient w.r.t layer weights
        grad_w = self.layer_input.T.dot(accum_grad)
        return grad_w

    def grad_b_dense(self, accum_grad):
        # Calculate gradient w.r.t layer weights
        grad_w0 = cp.sum(accum_grad, axis=0, keepdims=True)
        return grad_w0

    def grad_a_dense(self, accum_grad):
        W = self.w.data
        accum_grad = accum_grad.dot(W.T)
        return accum_grad

    def update_pass(self):
        # Update the layer weights
        if self.trainable:
            self.w = self.w_opt.update(self.w)
            self.b = self.b_opt.update(self.b)
        # clear the gradients
        self.zero_grad()

    def output_shape(self):
        return (self.n_units, )
