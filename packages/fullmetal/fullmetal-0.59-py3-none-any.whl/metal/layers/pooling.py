import numpy as np
from metal.layers.layer import LayerBase
from metal.utils.utils import pad2D
from metal.utils.functional import _pool2D_V1_, _pool2D_V1_backward

class Pool2D(LayerBase):
    def __init__(self, kernel_shape, stride=1, pad=0, mode="max", optimizer=None):
        """
        A single two-dimensional pooling layer.
        Parameters
        ----------
        kernel_shape : 2-tuple
            The dimension of a single 2D filter/kernel in the current layer
        stride : int
            The stride/hop of the convolution kernels as they move over the
            input volume. Default is 1.
        pad : int, tuple, or 'same'
            The number of rows/columns of 0's to pad the input. Default is 0.
        mode : {"max", "average"}
            The pooling function to apply.
        optimizer : str, :doc:`Optimizer <numpy_ml.neural_nets.optimizers>` object, or None
            The optimization strategy to use when performing gradient updates
            within the :meth:`update` method.  If None, use the :class:`SGD
            <numpy_ml.neural_nets.optimizers.SGD>` optimizer with
            default parameters. Default is None.
        """
        super().__init__(optimizer)

        self.pad = pad
        self.mode = mode
        self.in_ch = None
        self.out_ch = None
        self.stride = stride
        self.kernel_shape = kernel_shape
        self.is_initialized = False

    def _init_params(self):
        self.derived_variables = {"out_rows": [], "out_cols": [], "out_ch": [],"in_rows": [], "in_cols": []}
        self.is_initialized = True

    @property
    def hyperparameters(self):
        """Return a dictionary containing the layer hyperparameters."""
        return {
            "layer": "Pool2D",
            "act_fn": None,
            "pad": self.pad,
            "mode": self.mode,
            "in_ch": self.in_ch,
            "out_ch": self.out_ch,
            "stride": self.stride,
            "kernel_shape": self.kernel_shape,
            "optimizer": {
                "cache": self.optimizer.cache,
                "hyperparameters": self.optimizer.hyperparameters,
            },
        }

    def forward(self, X, retain_derived=True):
        """
        Compute the layer output given input volume `X`.
        Parameters
        ----------
        X : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, in_rows, in_cols, in_ch)`
            The input volume consisting of `n_ex` examples, each with dimension
            (`in_rows`,`in_cols`, `in_ch`)
        retain_derived : bool
            Whether to retain the variables calculated during the forward pass
            for use later during backprop. If False, this suggests the layer
            will not be expected to backprop through wrt. this input. Default
            is True.
        Returns
        -------
        Y : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, out_rows, out_cols, out_ch)`
            The layer output.
        """
        if not self.is_initialized:
            self.in_ch = self.out_ch = X.shape[3]
            self._init_params()

        n_ex, in_rows, in_cols, nc_in = X.shape
        (fr, fc), s, p = self.kernel_shape, self.stride, self.pad
        X_pad, (pr1, pr2, pc1, pc2) = pad2D(X, p, self.kernel_shape, s)

        out_rows = np.floor(1 + (in_rows + pr1 + pr2 - fr) / s).astype(int)
        out_cols = np.floor(1 + (in_cols + pc1 + pc2 - fc) / s).astype(int)

        cache = {}
        Y, cache = _pool2D_V1_(X,self.kernel_shape,out_rows, out_cols,nc_in,self.stride,self.mode,retain_derived,cache)

        if retain_derived:
            cache['a_prev'] = X
            self.X.append(cache)
            self.derived_variables["out_rows"].append(out_rows)
            self.derived_variables["out_cols"].append(out_cols)
            self.derived_variables["in_rows"].append(in_rows)
            self.derived_variables["in_cols"].append(in_cols)
            self.derived_variables["out_ch"].append(self.out_ch)
        return Y



    def backward(self, dLdY, retain_grads=True):
        """
        Backprop from layer outputs to inputs
        Parameters
        ----------
        dLdY : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, in_rows, in_cols, in_ch)`
            The gradient of the loss wrt. the layer output `Y`.
        retain_grads : bool
            Whether to include the intermediate parameter gradients computed
            during the backward pass in the final parameter update. Default is
            True.
        Returns
        -------
        dX : :py:class:`ndarray <numpy.ndarray>` of shape `(n_ex, in_rows, in_cols, in_ch)`
            The gradient of the loss wrt. the layer input `X`.
        """
        assert self.trainable, "Layer is frozen"
        if not isinstance(dLdY, list):
            dLdY = [dLdY]

        Xs = self.X[0]
        out_rows = self.derived_variables["out_rows"]
        out_cols = self.derived_variables["out_cols"]
        out_ch = self.derived_variables["out_ch"]

        in_rows = self.derived_variables["in_rows"]
        in_cols = self.derived_variables["in_cols"]


        return _pool2D_V1_backward(dLdY[0],Xs, in_rows[0], in_cols[0], out_ch[0], self.stride, self.kernel_shape, self.mode,out_rows[0],out_cols[0])
