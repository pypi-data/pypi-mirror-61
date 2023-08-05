from __future__ import division
import cupy as cp
from metalgpu.utils.data_operation import accuracy_score
from metalgpu.layers.activation_functions import Sigmoid
from autogradgpu.dependency import Dependency

class Loss(object):
    def loss(self, y, p):
        return NotImplementedError()

    def gradient(self, y, p):
        raise NotImplementedError()

    def acc(self, y, p):
        return 0

class SquareLoss(Loss):
    __slots__ = ('y','p','type')
    def __init__(self,y=None,p=None):
        self.y = y
        self.p = p
        self.type = type(p)

    def __call__(self,y=None,p=None):
        self.y = y
        self.p = p
        self.type = type(p)


    def loss(self):
        data = cp.mean(0.5 * cp.power((y.data - p.data), 2))
        requires_grad = self.p.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.p, self.gradient_SquareLoss)]
        else:
            depends_on = []
        return  self.type(data=data,requires_grad=requires_grad,depends_on=depends_on)


    def gradient_SquareLoss(self,grad):
        return -(self.y - self.p)

class CrossEntropy(Loss):
    __slots__ = ('y','p','type')
    def __init__(self,y=None,p=None):
        self.y = y
        self.p = p
        self.type = type(p)

    def __call__(self,y=None,p=None):
        self.y = y
        self.p = p
        self.type = type(p)

    def loss(self, training):
        # Avoid division by zero
        p = cp.clip(self.p.data.astype('float64'), 1e-15, 1 - 1e-15)
        data = cp.mean(- self.y.data.astype('float64') * cp.log(p) - (1 - self.y.data.astype('float64')) * cp.log(1 - p))
        requires_grad = self.p.requires_grad
        if training:
            if requires_grad:
                depends_on = [Dependency(self.p, self.gradient_CrossEntropy)]
            else:
                depends_on = []
        else:
            depends_on = []
        return  self.type(data=data,requires_grad=requires_grad,depends_on=depends_on)

    def gradient_CrossEntropy(self,grad):
        # Avoid division by zero
        p = cp.clip(self.p.data.astype('float64'), 1e-15, 1 - 1e-15)
        d = - (self.y.data.astype('float64') / p) + (1 - self.y.data.astype('float64')) / (1 - p) * grad.astype('float64')
        return d.astype('float32')

    def acc(self):
        return accuracy_score(cp.argmax(self.y.data, axis=1), cp.argmax(self.p.data, axis=1))
