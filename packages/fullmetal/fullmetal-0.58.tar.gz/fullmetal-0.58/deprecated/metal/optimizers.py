# Optimizers for models that use gradient based methods for finding the
# weights that minimizes the loss.
# A great resource for understanding these methods:
# http://sebastianruder.com/optimizing-gradient-descent/index.html

import numpy as np
from autograd.tensor import Tensor

class StochasticGradientDescent():
    __slots__ = ('learning_rate','momentum','w_updt')
    def __init__(self, learning_rate=0.01, momentum=0):
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.w_updt = None

    def update(self, w):
        # If not initialized
        if self.w_updt is None:
            self.w_updt = np.zeros(np.shape(w.data))
        # Use momentum if set
        self.w_updt = w.grad  * (1 - self.momentum) + self.momentum * self.w_updt
        # Move against the gradient to minimize loss
        return w - self.learning_rate * self.w_updt

class Adam():
    __slots__ = ('learning_rate','eps','m','v','b1','b2','w_updt')
    def __init__(self, learning_rate=0.001, b1=0.9, b2=0.999):
        self.learning_rate = learning_rate
        self.eps = 1e-8
        self.m = None
        self.v = None
        # Decay rates
        self.b1 = b1
        self.b2 = b2

    def update(self, w):
        # If not initialized
        if self.m is None:
            self.m = np.zeros(np.shape(w.grad.data))
            self.v = np.zeros(np.shape(w.grad.data))

        self.m = w.grad * (1 - self.b1) + self.b1 * self.m
        self.v = (w.grad * w.grad) * (1 - self.b2) + self.b2 * self.v

        m_hat = self.m / (1 - self.b1)
        v_hat = self.v / (1 - self.b2)

        self.w_updt =  m_hat * self.learning_rate  / (np.sqrt(v_hat.data) + self.eps)

        return w - self.w_updt
