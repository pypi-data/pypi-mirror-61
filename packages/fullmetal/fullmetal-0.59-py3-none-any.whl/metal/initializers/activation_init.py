import numpy as np
import re
from metal.activations.activation import ActivationBase, Affine, ReLU, Sigmoid, Tanh

class ActivationInitializer(object):
    def __init__(self, param=None):
        """
        A class for initializing activation functions. Valid inputs are:
            (a) __str__ representations of `ActivationBase` instances
            (b) `ActivationBase` instances
        If `param` is `None`, return the identity function: f(X) = X
        """
        self.param = param

    def __call__(self):
        param = self.param
        if param is None:
            act = Affine(slope=1, intercept=0)
        elif isinstance(param, ActivationBase):
            act = param
        elif isinstance(param, str):
            act = self.init_from_str(param)
        else:
            raise ValueError("Unknown activation: {}".format(param))
        return act

    def init_from_str(self, act_str):
        act_str = act_str.lower()
        if act_str == "relu":
            act_fn = ReLU()
        elif act_str == "tanh":
            act_fn = Tanh()
        elif act_str == "sigmoid":
            act_fn = Sigmoid()
        elif "affine" in act_str:
            r = r"affine\(slope=(.*), intercept=(.*)\)"
            slope, intercept = re.match(r, act_str).groups()
            act_fn = Affine(float(slope), float(intercept))
        elif "leaky relu" in act_str:
            r = r"leaky relu\(alpha=(.*)\)"
            alpha = re.match(r, act_str).groups()[0]
            act_fn = LeakyReLU(float(alpha))
        else:
            raise ValueError("Unknown activation: {}".format(act_str))
        return act_fn
