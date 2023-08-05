
import numpy as np
from autograd.node import Node


class Parameter(Node):
    def __init__(self, data=None, requires_grad=True, depends_on=None, create_array=None, name=None):
        self.name = name
        if create_array is not None:
            np.random.seed(create_array[0])
            data_ = np.random.randn(*create_array)
        elif data is not None:
            data_ = data
        super().__init__(data=data_, requires_grad=requires_grad, depends_on=depends_on)

    def __repr__(self) -> str:
        return f"Parameter({self.data}, requires_grad={self.requires_grad})"
