
from typing import List, NamedTuple, Callable, Optional, Union
import numpy as np

class Dependency(NamedTuple):
    Node: "Tensor"
    grad_fn: Callable[[np.ndarray], np.ndarray]
