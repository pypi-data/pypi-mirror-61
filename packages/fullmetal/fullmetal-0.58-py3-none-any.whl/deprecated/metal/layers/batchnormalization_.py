import numpy as np
from autograd.tensor import Tensor
from autograd.parameter import Parameter
from deprecated.metal.module import Module
from autograd.dependency import Dependency
import math
import copy
from deprecated.metal.layers.layer import Layer


class BatchNormalization(Layer):
    __slots__ = ('momentum','trainable','eps','running_mean','running_var','gamma','beta','gamma_opt','beta_opt','type','running_mean','running_var','X_centered','stddev_inv')
    """
    Batch normalization.
    """
    def __init__(self, momentum=0.99):
        self.momentum = momentum
        self.trainable = True
        self.eps = 0.01
        self.running_mean = None
        self.running_var = None

    def initialize(self, optimizer):
        # Initialize the parameters
        self.gamma = Parameter(np.ones(self.input_shape))
        self.beta = Parameter(np.zeros(self.input_shape))
        # parameter optimizers
        self.gamma_opt  = copy.copy(optimizer)
        self.beta_opt = copy.copy(optimizer)


    def forward_pass(self, x, training=True):
        # Initialize running mean and variance if first run
        X = x.data
        self.type = type(x)
        requires_grad = x.requires_grad or self.gamma.requires_grad or self.beta.requires_grad
        depends_on: List[Dependency] = []

        if self.running_mean is None:
            self.running_mean = np.mean(X, axis=0)
            self.running_var = np.var(X, axis=0)

        if training and self.trainable:
            mean = np.mean(X, axis=0)
            var = np.var(X, axis=0)
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * var
        else:
            mean = self.running_mean
            var = self.running_var

        # Statistics saved for backward pass
        self.X_centered = X - mean
        self.stddev_inv = 1 / np.sqrt(var + self.eps)

        X_norm = self.X_centered * self.stddev_inv
        data = self.gamma.data * X_norm + self.beta.data
        if training:
            if requires_grad:
                if self.gamma.requires_grad:
                    depends_on.append(Dependency(self.gamma, self.grad_gamma_batchNorm))
                if self.beta.requires_grad:
                    depends_on.append(Dependency(self.beta, self.grad_beta_batchNorm))
                if x.requires_grad:
                    depends_on.append(Dependency(x, self.grad_x_batchNorm))
            else:
                depends_on = []
        else:
            depends_on = []
        return self.type(data=data,requires_grad=requires_grad,depends_on=depends_on)


    def grad_gamma_batchNorm(self, grad):
        # Save parameters used during the forward pass
        X_norm = self.X_centered * self.stddev_inv
        grad_gamma = np.sum(grad * X_norm, axis=0)
        return grad_gamma


    def grad_beta_batchNorm(self, grad):
        # Save parameters used during the forward pass
        grad_beta = np.sum(grad, axis=0)
        return grad_beta

    def grad_x_batchNorm(self, grad):
        # Save parameters used during the forward pass
        gamma = self.gamma.data
        batch_size = grad.shape[0]
        # The gradient of the loss with respect to the layer inputs (use weights and statistics from forward pass)
        accum_grad = (1 / batch_size) * gamma * self.stddev_inv * (
            batch_size * grad
            - np.sum(grad, axis=0)
            - self.X_centered * self.stddev_inv**2 * np.sum(grad * self.X_centered, axis=0)
            )

        return accum_grad

    def update_pass(self):
        # If the layer is trainable the parameters are updated
        if self.trainable:
            self.gamma = self.gamma_opt.update(self.gamma)
            self.beta = self.beta_opt.update(self.beta)
        # clear the gradients
        self.zero_grad()

    def output_shape(self):
        return self.input_shape
