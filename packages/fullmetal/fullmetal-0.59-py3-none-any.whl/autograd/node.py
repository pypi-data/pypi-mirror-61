from __future__ import division
from typing import List, NamedTuple, Callable, Optional, Union
import numpy as np
from autograd.math_operations import Sum, Add, MatMul, Mul, Sub, Div, Neg, Exp, Max
from autograd.tensor_modifications import Slice, T, Reshape, Pad
from autograd.dependency import Dependency
from autograd.engin import  autograd


Arrayable = Union[float, list, np.ndarray]


def ensure_array(arrayable: Arrayable) -> np.ndarray:
    if isinstance(arrayable, np.ndarray):
        arrayable =  arrayable.astype(np.float32, copy=False)
        return arrayable
    else:
        return np.array(arrayable).astype(np.float32, copy=False)


Nodeable = Union["Node", float, np.ndarray]


def ensure_Type(Nodeable: Nodeable, t) -> "Node":
    if isinstance(Nodeable, Node):
        return Nodeable
    else:
        TYPE = type(t)
        return TYPE(Nodeable, requires_grad=False)



class Node(object):
    __slots__ = ('_data','requires_grad','depends_on','shape','grad','name','id')
    def __init__(self,data: Arrayable,requires_grad: bool = False,depends_on: List[Dependency] = None, id = None, name=None) -> None:
        self._data = ensure_array(data)
        self.requires_grad = requires_grad
        self.depends_on = depends_on or []
        self.shape = self._data.shape
        self.grad: Optional["Node"] = None
        self.name = name
        if id is None:
            id = np.random.randint(0, 100_000)
        self.id = id
        if self.requires_grad:
            self.zero_grad()

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, new_data: np.ndarray) -> None:
        self._data = new_data
        # Setting the data manually means we invalidate the gradient.
        self.grad = None

    def zero_grad(self) -> None:
        self.type = type(self)
        self.grad = self.type(np.zeros_like(self.data, dtype=np.float32),requires_grad=False)

    def __repr__(self) -> str:
        return f"Node({self.data}, requires_grad={self.requires_grad})"

    def __add__(self, other) -> "Node":
        """gets called if I do t + other"""
        return Add(self,ensure_Type(other,self))._add()

    def __radd__(self, other) -> "Node":
        """gets called if I do other + t"""
        return Add(ensure_Type(other,self), self)._add()

    def __iadd__(self, other) -> "Node":
        """when we do t += other"""
        self.data = self.data + ensure_Type(other,self).data
        return self

    def __isub__(self, other) -> "Node":
        """when we do t -= other"""
        self.data = self.data - ensure_Type(other,self).data
        return self

    def __imul__(self, other) -> "Node":
        """when we do t *= other"""
        self.data = self.data * ensure_Type(other,self).data
        return self

    def __mul__(self, other) -> "Node":
        return Mul(self, ensure_Type(other,self))._mul()

    def __rmul__(self, other) -> "Node":
        return Mul(ensure_Type(other,self), self)._mul()

    def __matmul__(self, other) -> "Node":
        return MatMul(self, other)._matmul()

    def __neg__(self) -> "Node":
        return Neg(self)._neg()

    def __sub__(self, other) -> "Node":
        return Sub(self, ensure_Type(other,self))._sub()

    def __rsub__(self, other) -> "Node":
        return Sub(self, ensure_Type(other,self))._sub()

    def __getitem__(self, idxs) -> "Node":
        return Slice(self, idxs)._slice()

    def __truediv__(self, other) -> "Node":
        """gets called if I do t / other"""
        return Div(self, ensure_Type(other,self))._div()

    def __rtruediv__(self, other) -> "Node":
        """gets called if I do other / t"""
        return Div(ensure_Type(other,self), self)._div()

    def sum(self,axis=None) -> "Node":
        return Sum(self,axis)._sum()

    def T(self,*axis) -> "Node":
        return T(self,axis)._T()

    def pad(self,*pad) -> "Node":
        return Pad(self,pad)._pad()

    def reshape(self,*newshape)-> "Node":
        return Reshape(self,newshape)._reshape()

    def exp(self)->"Node":
        return Exp(self)._exp()

    def max(self)->"Node":
        return Max(self)._max()

    def backward(self, grad: "Node" = None) -> None:
        autograd(self).backward(grad) # apply backward function wrapping the output gardent
