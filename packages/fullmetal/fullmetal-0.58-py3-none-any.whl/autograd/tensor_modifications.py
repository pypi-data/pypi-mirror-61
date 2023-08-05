
import numpy as np
from autograd.dependency import Dependency
import math

class Slice(object):
    __slots__ = ('type','t','name','idxs')

    """docstring for Slice."""
    def __init__(self, t, idxs, name_child=None):
        self.type = type(t)
        self.t = t
        self.name = name_child
        self.idxs = idxs

    def _slice(self):
        data = self.t.data[self.idxs]
        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, self.grad_slice)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_slice(self, grad: np.ndarray) -> np.ndarray:
        old_shape = self.t.shape
        new_grad = np.zeros(old_shape, dtype=np.float32)
        new_grad[self.idxs] = grad
        return new_grad


class T(object):
    __slots__ = ('type','t','axis','name')

    """docstring for Transpose."""
    def __init__(self, t, axis, name_child=None):
        self.type = type(t)
        self.t = t
        self.axis = axis
        self.name = name_child

    def _T(self):
        data = self.t.data.transpose(*self.axis)
        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, self.grad_t)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_t(self, grad: np.ndarray):
        return grad.reshape(self.t.data.shape)

class Reshape(object):
    __slots__ = ('type','new_shape','t','name')

    """docstring for Reshape."""
    def __init__(self, t, newshape, name_child=None):
        super(Reshape, self).__init__()
        self.type = type(t)
        self.new_shape = newshape
        self.t = t
        self.name = name_child


    def _reshape(self):
        data = self.t.data.reshape(*self.new_shape)
        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, self.grad_reshape)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_reshape(self, grad: np.array):
        old_shape = self.t.shape
        return grad.reshape(*old_shape)
        #return grad.transpose([x for x in range(self.t.data.ndim)])

class Pad(object):
    __slots__ = ('type','t','pad','name')

    """docstring for Pad."""
    def __init__(self, t, pad, name_child=None):
        super(Pad, self).__init__()
        self.type = type(t)
        self.t = t
        self.pad = pad
        self.name = name_child

    def _pad(self):
        data = np.pad(self.t.data, self.pad[0], mode=self.pad[1])
        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, self.grad_pad)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name=self.name )

    def grad_pad(self, grad: np.array):
        slices = []
        for c in self.pad[0]:
            e = None if c[1] == 0 else -c[1]
            slices.append(slice(c[0], e))
        return grad[tuple(slices)]
