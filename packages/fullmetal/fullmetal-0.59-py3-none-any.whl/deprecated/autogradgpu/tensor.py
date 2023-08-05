
from typing import List
import cupy as cp
from autogradgpu.node import Node
from autogradgpu.dependency import Dependency


class Tensor(Node):
    """docstring for Tensor."""
    def __init__(self, data: cp.ndarray, requires_grad: bool = False, depends_on: List[Dependency] = None, name=None):
        super().__init__(data=data,requires_grad=requires_grad, depends_on=depends_on)
        self.name = name

    def __repr__(self) -> str:
        return f"Tensor({self.data}, requires_grad={self.requires_grad})"
