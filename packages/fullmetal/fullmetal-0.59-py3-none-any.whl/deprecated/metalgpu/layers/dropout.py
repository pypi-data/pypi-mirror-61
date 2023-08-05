import cupy as cp
from autogradgpu.tensor import Tensor
from autogradgpu.parameter import Parameter
from autogradgpu.dependency import Dependency
import math
import copy
from metalgpu.layers.layer import Layer


class Dropout(Layer):
    __slots__ =( 'p', '_mask','n_units', 'pass_through','trainable','type' )

    """A layer that randomly sets a fraction p of the output units of the previous layer
    to zero.
    Parameters:
    -----------
    p: float
        The probability that unit x is set to zero.
    """
    def __init__(self, p=0.2):
        self.p = p
        self._mask = None
        self.input_shape = None
        self.n_units = None
        self.pass_through = True
        self.trainable = True

    def forward_pass(self, X, training=True):
        requires_grad =  X.requires_grad
        self.type = type(X)
        c = (1 - self.p)
        if training:
            self._mask = cp.random.uniform(size=X.shape) > self.p
            c = self._mask
        data =  X.data * c

        if requires_grad:
            depends_on = [Dependency(X, self.grad_dropout)]
        else:
            depends_on = []
        return self.type(data=data,requires_grad=requires_grad,depends_on=depends_on)

    def grad_dropout(self, accum_grad):
        return accum_grad * self._mask

    def update_pass(self):
        # clear the gradients
        self.zero_grad()

    def output_shape(self):
        return self.input_shape
