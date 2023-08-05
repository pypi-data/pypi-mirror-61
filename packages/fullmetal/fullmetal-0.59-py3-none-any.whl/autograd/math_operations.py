
import numpy as np
from autograd.dependency import Dependency


class Sum(object):
    __slots__ = ('type','t','axis','name','t_shape')

    def __init__(self, t, axis, name_child=None):
        self.type = type(t)
        self.t = t
        self.axis = axis
        self.name = name_child
        self.t_shape = None


    def _sum(self):
        #Takes a Tensor and returns the 0-Tensor that's the sum of all its elements.
        if self.axis == None:
            data = self.t.data.sum()
            self.t_shape = self.t.shape
        else:
            data = self.t.data.sum(axis=self.axis)
            self.t_shape = data.shape

        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, self.grad_sum)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_sum(self, grad: np.ndarray) -> np.ndarray:
        #grad is necessarily a 0-Tensor, so each input element contributes that much
        return grad * np.ones(self.t_shape)


class Add(object):
    __slots__ = ('type','t1','t2','name')

    def __init__(self, t1, t2, name_child=None):
        self.type = type(t1)
        self.t1 = t1
        self.t2 = t2
        self.name = name_child

    def _add(self):
        data = self.t1.data + self.t2.data
        requires_grad = self.t1.requires_grad or self.t2.requires_grad
        depends_on: List[Dependency] = []

        if self.t1.requires_grad:
            depends_on.append(Dependency(self.t1, self.grad_add1))
        if self.t2.requires_grad:
            depends_on.append(Dependency(self.t2, self.grad_add2))
        return self.type(data, requires_grad, depends_on, name=self.name)


    def grad_add1(self, grad: np.ndarray) -> np.ndarray:
        # Sum out added dims
        ndims_added = grad.ndim - self.t1.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t1.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad

    def grad_add2(self, grad: np.ndarray) -> np.ndarray:
        # Sum out added dims
        ndims_added = grad.ndim - self.t2.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t2.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad

class Mul(object):
    __slots__ = ('type','t1','t2','name')

    def __init__(self, t1, t2, name_child=None):
        self.type = type(t1)
        self.t1 = t1
        self.t2 = t2
        self.name = name_child

    def _mul(self):
        data = self.t1.data * self.t2.data
        requires_grad = self.t1.requires_grad or self.t2.requires_grad
        depends_on: List[Dependency] = []

        if self.t1.requires_grad:
            depends_on.append(Dependency(self.t1, self.grad_mul1))
        if self.t2.requires_grad:
            depends_on.append(Dependency(self.t2, self.grad_mul2))
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_mul1(self, grad: np.ndarray) -> np.ndarray:
        grad = grad * self.t2.data
        # Sum out added dims
        ndims_added = grad.ndim - self.t1.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t1.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad

    def grad_mul2(self, grad: np.ndarray) -> np.ndarray:
        grad = grad * self.t1.data
        # Sum out added dims
        ndims_added = grad.ndim - self.t2.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t2.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad


class Neg(object):
    __slots__ = ('type','t','name')

    def __init__(self, t, name_child=None):
        self.type = type(t)
        self.t = t
        self.name = name_child

    def _neg(self):
        data = -self.t.data
        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, lambda x: -x)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name=self.name)

class Sub(object):
    __slots__ = ('type','t1','t2','name')

    def __init__(self, t1, t2, name_child=None):
        self.type = type(t1)
        self.t1 = t1
        self.t2 = t2
        self.name = name_child

    def _sub(self):
        t3 = self.t1 + -self.t2
        t3.name = self.name
        return t3

class MatMul(object):
    __slots__ = ('type','t1','t2','name')

    def __init__(self, t1, t2, name_child = None):
        self.type = type(t1)
        self.t1 = t1
        self.t2 = t2
        self.name = name_child


    def _matmul(self):
        """
        if t1 is (n1, m1) and t2 is (m1, m2), then t1 @ t2 is (n1, m2)
        so grad3 is (n1, m2)
        if t3 = t1 @ t2, and grad3 is the gradient of some function wrt t3, then
            grad1 = grad3 @ t2.T
            grad2 = t1.T @ grad3
        """
        data = self.t1.data.dot(self.t2.data)
        requires_grad = self.t1.requires_grad or self.t2.requires_grad
        depends_on: List[Dependency] = []

        if self.t1.requires_grad:
            depends_on.append(Dependency(self.t1, self.grad_mm1))
        if self.t2.requires_grad:
            depends_on.append(Dependency(self.t2, self.grad_mm2))
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_mm1(self, grad: np.ndarray) -> np.ndarray:
        return grad.dot(self.t2.data.T)

    def grad_mm2(self, grad: np.ndarray) -> np.ndarray:
        return self.t1.data.T.dot(grad)

class Div(object):
    __slots__ = ('type','t1','t2','name')

    def __init__(self, t1, t2, name_child = None):
        self.type = type(t1)
        self.t1 = t1
        self.t2 = t2
        self.name = name_child

    def _div(self):
        data = self.t1.data / self.t2.data
        requires_grad = self.t1.requires_grad or self.t2.requires_grad
        depends_on: List[Dependency] = []
        if self.t1.requires_grad:
            depends_on.append(Dependency(self.t1, self.grad_div1))
        if self.t2.requires_grad:
            depends_on.append(Dependency(self.t2, self.grad_div2))
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_div1(self, grad: np.ndarray) -> np.ndarray:
        grad = grad * (1 / self.t2.data)
        # Sum out added dims
        ndims_added = grad.ndim - self.t1.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t1.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad

    def grad_div2(self, grad: np.ndarray) -> np.ndarray:
        grad = grad * (-self.t1.data / (self.t2.data * self.t2.data))
        # Sum out added dims
        ndims_added = grad.ndim - self.t2.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t2.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad



class Exp(object):
    __slots__ = ('type','t','name')

    """docstring for Exp."""
    def __init__(self, t,  name_child = None):
        self.type = type(t)
        self.t = t
        self.name = name_child

    def _exp(self):
        data = np.exp(self.t.data)
        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, self.grad_exp)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name = self.name)

    def grad_exp(self, grad: np.array):
        grad = grad * np.exp(self.t.data)
        # Sum out added dims
        ndims_added = grad.ndim - self.t.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad


class Max(object):
    __slots__ = ('type','t','name')

    """docstring for Max."""
    def __init__(self, t, name_child = None):
        self.type = type(t)
        self.t = t
        self.name = name_child

    def _max(self):
        data = self.t.data.max()
        requires_grad = self.t.requires_grad
        if requires_grad:
            depends_on = [Dependency(self.t, self.grad_max)]
        else:
            depends_on = []
        return self.type(data, requires_grad, depends_on, name=self.name)

    def grad_max(self, grad: np.array):
        grad = np.equal(self.t.data, self.t.data.max()) * grad.sum()
        # Sum out added dims
        ndims_added = grad.ndim - self.t.data.ndim
        for _ in range(ndims_added):
            grad = grad.sum(axis=0)
        # Sum across broadcasted (but non-added dims)
        for i, dim in enumerate(self.t.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
        return grad
