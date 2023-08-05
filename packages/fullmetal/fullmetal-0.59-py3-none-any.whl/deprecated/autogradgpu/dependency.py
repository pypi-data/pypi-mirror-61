
from typing import List, NamedTuple, Callable, Optional, Union
import cupy as cp

class Dependency(NamedTuple):
    Node: "Tensor"
    grad_fn: Callable[[cp.ndarray], cp.ndarray]
