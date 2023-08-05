import numpy as np
from autograd.tensor import Tensor
from autograd.parameter import Parameter
from deprecated.metal.module import Module
from autograd.dependency import Dependency
import math
import copy
from deprecated.metal.layers.activation_functions import Sigmoid, ReLU, TanH, Softmax
from deprecated.metal.utils.layer_data_manipulations import *


activation_functions = {
    'relu': ReLU,
    'sigmoid': Sigmoid,
    'tanh': TanH,
    'softmax':Softmax,
}

class Layer(Module):
    __slots__ = ('input_shape')
    """docstring for Layer."""

    def set_input_shape(self, shape):
        """ Sets the shape that the layer expects of the input in the forward
        pass method """
        self.input_shape = shape

    def layer_name(self):
        """ The name of the layer. Used in model summary. """
        return self.__class__.__name__

    def parameters_(self):
        """ The number of trainable parameters used by the layer """
        return 0

    def forward_pass(self, X, training):
        """ Propogates the signal forward in the network """
        raise NotImplementedError()

    def update_pass(self):
        """ Propogates the accumulated gradient backwards in the network.
        If the has trainable weights then these weights are also tuned in this method.
        As input (accum_grad) it receives the gradient with respect to the output of the layer and
        returns the gradient with respect to the output of the previous layer. """
        raise NotImplementedError()

    def output_shape(self):
        """ The shape of the output produced by forward_pass """
        raise NotImplementedError()



class Activation(Layer):
    __slots__=('activation_name','activation_func','trainable','layer_input')
    """A layer that applies an activation operation to the input.

    Parameters:
    -----------
    name: string
        The name of the activation function that will be used.
    """

    def __init__(self, name):
        self.activation_name = name
        self.activation_func = activation_functions[name]()
        self.trainable = True

    def layer_name(self):
        return "Activation (%s)" % (self.activation_func.__class__.__name__)

    def forward_pass(self, X, training):
        return self.activation_func(X, training)

    def update_pass(self):
        self.zero_grad()

    def output_shape(self):
        return self.input_shape

class PoolingLayer(Layer):
    """A parent class of MaxPooling2D and AveragePooling2D
    """
    def __init__(self, pool_shape=(2, 2), stride=1, padding=0):
        self.pool_shape = pool_shape
        self.stride = stride
        self.padding = padding
        self.trainable = True

    def forward_pass(self, x, training=True):
        self.layer_input = x
        X = x.data
        self.type = type(x)

        requires_grad = x.requires_grad

        batch_size, channels, height, width = X.shape

        _, out_height, out_width = self.output_shape()

        X = X.reshape(batch_size*channels, 1, height, width)
        X_col = image_to_column(X, self.pool_shape, self.stride, self.padding)

        # MaxPool or AveragePool specific method
        output = self._pool_forward(X_col)

        output = output.reshape(out_height, out_width, batch_size, channels)
        output = output.transpose(2, 3, 0, 1)

        if training:
            if requires_grad:
                depends_on = [Dependency(x, self.grad_pool)]
            else:
                depends_on = []
        else:
            depends_on = []

        return self.type(data=output, requires_grad=requires_grad, depends_on=depends_on)

    def grad_pool(self, accum_grad):
        batch_size, _, _, _ = accum_grad.shape
        channels, height, width = self.input_shape
        accum_grad = accum_grad.transpose(2, 3, 0, 1).ravel()

        # MaxPool or AveragePool specific method
        accum_grad_col = self._pool_backward(accum_grad)

        accum_grad = column_to_image(accum_grad_col, (batch_size * channels, 1, height, width), self.pool_shape, self.stride, self.padding)
        accum_grad = accum_grad.reshape((batch_size,) + self.input_shape)

        return accum_grad

    def update_pass(self):
        pass

    def output_shape(self):
        channels, height, width = self.input_shape
        out_height = (height - self.pool_shape[0]) / self.stride + 1
        out_width = (width - self.pool_shape[1]) / self.stride + 1
        assert out_height % 1 == 0
        assert out_width % 1 == 0
        return channels, int(out_height), int(out_width)
