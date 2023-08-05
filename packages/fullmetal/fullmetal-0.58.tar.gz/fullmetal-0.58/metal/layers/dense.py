import numpy as np

from metal.layers.layer import LayerBase
from metal.initializers.activation_init import ActivationInitializer
from metal.initializers.weight_init import WeightInitializer
from metal.utils.utils import dtype

class Dense(LayerBase):
    def __init__(self, n_out, act_fn=None, init="glorot_uniform", optimizer=None):
        """
        A fully-connected (dense) layer.
        Notes
        -----
        A fully connected layer computes the function
        .. math::
            \mathbf{Y} = f( \mathbf{WX} + \mathbf{b} )
        where `f` is the activation nonlinearity, **W** and **b** are
        parameters of the layer, and **X** is the minibatch of input examples.
        Parameters
        ----------
        n_out : int
            The dimensionality of the layer output
        act_fn : str, :doc:`Activation <numpy_ml.neural_nets.activations>` object, or None
            The element-wise output nonlinearity used in computing `Y`. If None,
            use the identity function :math:`f(X) = X`. Default is None.
        init : {'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'}
            The weight initialization strategy. Default is `'glorot_uniform'`.
        optimizer : str, :doc:`Optimizer <numpy_ml.neural_nets.optimizers>` object, or None
            The optimization strategy to use when performing gradient updates
            within the :meth:`update` method.  If None, use the :class:`SGD
            <numpy_ml.neural_nets.optimizers.SGD>` optimizer with
            default parameters. Default is None.
        """
        super().__init__(optimizer)

        self.init = init
        self.n_in = None
        self.n_out = n_out
        self.act_fn = ActivationInitializer(act_fn)()
        self.parameters = {"W": None, "b": None}
        self.is_initialized = False


    def _init_params(self):
        init_weights = WeightInitializer(str(self.act_fn), mode=self.init)

        b = dtype(np.zeros((1, self.n_out)))
        W = dtype(init_weights((self.n_in, self.n_out)))

        self.parameters = {"W": W, "b": b}
        self.derived_variables = {"Z": []}
        self.gradients = {"W": np.zeros_like(W), "b": np.zeros_like(b)}
        self.is_initialized = True

    @property
    def hyperparameters(self):
        """Return a dictionary containing the layer hyperparameters."""
        return {
            "layer": "FullyConnected",
            "init": self.init,
            "n_in": self.n_in,
            "n_out": self.n_out,
            "act_fn": str(self.act_fn),
            "optimizer": {
                "cache": self.optimizer.cache,
                "hyperparameters": self.optimizer.hyperparameters,
            },
        }

    def forward(self, X, retain_derived=True):
        """
        Compute the layer output on a single minibatch.
        Parameters
        ----------
        X : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, n_in)`
            Layer input, representing the `n_in`-dimensional features for a
            minibatch of `n_ex` examples.
        retain_derived : bool
            Whether to retain the variables calculated during the forward pass
            for use later during backprop. If False, this suggests the layer
            will not be expected to backprop through wrt. this input. Default
            is True.
        Returns
        -------
        Y : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, n_out)`
            Layer output for each of the `n_ex` examples.
        """
        if not self.is_initialized:
            self.n_in = X.shape[1]
            self._init_params()

        Y, Z = self._fwd(X)

        if retain_derived:
            self.X.append(X)
            self.derived_variables["Z"].append(Z)

        return Y

    def _fwd(self, X):
        """Actual computation of forward pass"""
        W = self.parameters["W"]
        b = self.parameters["b"]

        Z = X @ W + b
        Y = self.act_fn(Z)
        return Y, Z

    def backward(self, dLdy, retain_grads=True):
        """
        Backprop from layer outputs to inputs.
        Parameters
        ----------
        dLdy : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, n_out)` or list of arrays
            The gradient(s) of the loss wrt. the layer output(s).
        retain_grads : bool
            Whether to include the intermediate parameter gradients computed
            during the backward pass in the final parameter update. Default is
            True.
        Returns
        -------
        dLdX : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, n_in)` or list of arrays
            The gradient of the loss wrt. the layer input(s) `X`.
        """
        assert self.trainable, "Layer is frozen"
        if not isinstance(dLdy, list):
            dLdy = [dLdy]

        dX = []
        X = self.X
        for dy, x in zip(dLdy, X):
            dx, dw, db = self._bwd(dy, x)
            dX.append(dx)

            if retain_grads:
                self.gradients["W"] += dw
                self.gradients["b"] += db

        return dX[0] if len(X) == 1 else dX

    def _bwd(self, dLdy, X):
        """Actual computation of gradient of the loss wrt. X, W, and b"""
        W = self.parameters["W"]
        b = self.parameters["b"]

        Z = X @ W + b
        dZ = dLdy * self.act_fn.grad(Z)

        dX = dZ @ W.T
        dW = X.T @ dZ
        dB = dZ.sum(axis=0, keepdims=True)
        return dX, dW, dB

    def _bwd2(self, dLdy, X, dLdy_bwd):
        """Compute second derivatives / deriv. of loss wrt. dX, dW, and db"""
        W = self.parameters["W"]
        b = self.parameters["b"]

        dZ = self.act_fn.grad(X @ W + b)
        ddZ = self.act_fn.grad2(X @ W + b)

        ddX = dLdy @ W * dZ
        ddW = dLdy.T @ (dLdy_bwd * dZ)
        ddB = np.sum(dLdy @ W * dLdy_bwd * ddZ, axis=0, keepdims=True)
        return ddX, ddW, ddB
