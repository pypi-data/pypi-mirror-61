import numpy as np
from autograd.tensor import Tensor
from autograd.dependency import Dependency

# Collection of activation functions
# Reference: https://en.wikipedia.org/wiki/Activation_function

class Sigmoid(object):
    __slots__ = ('TYPE','data')
    """docstring for Sigmoid."""

    def __call__(self, x, training):
        self.TYPE = type(x)
        requires_grad = x.requires_grad
        self.data =  1 / (1 + np.exp(-x.data))
        if training:
            if requires_grad:
                depends_on = [Dependency(x, self.grad_sigmoid)]
            else:
                depends_on = []
        else:
            depends_on = []
        return self.TYPE(data=self.data,requires_grad=requires_grad,depends_on=depends_on)

    def grad_sigmoid(self, grad):
        return (self.data * (1 - self.data)) * grad


class TanH(object):
    __slots__ = ('TYPE','data')
    """docstring for TanH."""

    def __call__(self, x):
        self.TYPE = type(x)
        requires_grad = x.requires_grad
        self.data = np.tanh(x.data)
        if requires_grad:
            depends_on = [Dependency(x, self.grad_tanh)]
        else:
            depends_on = []
        return self.TYPE(data=self.data,requires_grad=requires_grad,depends_on=depends_on)

    def grad_tanh(self, grad):
        return (1 - self.data**2) * grad



class ReLU(object):
    __slots__ = ('type','x')

    """docstring for ReLU."""

    def __call__(self,x,training):
        self.x = x.data
        self.type = type(x)
        requires_grad = x.requires_grad

        data  = self.x * (self.x > 0)
        if training:
            if requires_grad:
                depends_on = [Dependency(x, self.grad_relu)]
            else:
                depends_on = []
        else:
            depends_on = []
        return self.type(data=data,requires_grad=requires_grad,depends_on=depends_on)

    def grad_relu(self, grad):
        return grad * (self.x>0)


class Softmax(object):
    __slots__ = ('TYPE','x')

    """docstring for Softmax."""

    def __call__(self, x, training):
        self.x = x.data
        self.TYPE = type(x)
        requires_grad = x.requires_grad

        e_x = np.exp(self.x - np.max(self.x, axis=-1, keepdims=True))
        e_x = e_x / np.sum(e_x, axis=-1, keepdims=True)
        if training:
            if requires_grad:
                depends_on = [Dependency(x, self.grad_softmax)]
            else:
                depends_on = []
        else:
            depends_on = []
        return self.TYPE(data=e_x,requires_grad=requires_grad,depends_on=depends_on)

    def grad_softmax(self, grad):
        e_x = np.exp(self.x - np.max(self.x, axis=-1, keepdims=True))
        e_x = e_x / np.sum(e_x, axis=-1, keepdims=True)
        return grad * (e_x * (1 - e_x))



"""
class LeakyReLU():
    def __call__(self, x, alpha=0.2):
        y1 = (x * (x.data > 0))
        y2 = (x * alpha * (x.data <= 0))
        return y1 + y2
"""

"""
class ReLU_():
    def __call__(self,x_):
        x = x_.data
        self.type = type(x_)
        requires_grad = x_.requires_grad
        if requires_grad:
            depends_on = [Dependency(x_, self.grad_relu)]
        else:
            depends_on = []
        return self.type(data=np.where(x >= 0, x, 0),requires_grad=requires_grad,depends_on=depends_on)

    def grad_relu(self, x):
        print(np.where(x >= 0, 1, 0))
        return np.where(x >= 0, 1, 0)
"""

# https://eli.thegreenplace.net/2016/the-softmax-function-and-its-derivative/
"""
class Softmax_():
    #docstring for Softmax.
    def __call__(self, x):
        shiftx = x - x.max()
        exps = shiftx.exp()
        return exps / exps.sum()
"""
