import cupy as cp
from metalgpu.layers.layer import PoolingLayer
import numpy as np

class MaxPooling2D(PoolingLayer):
    def _pool_forward(self, X_col):
        X_col = cp.asnumpy(X_col)
        arg_max = np.argmax(X_col, axis=0).flatten()
        output = X_col[arg_max, range(arg_max.size)]
        self.cache = arg_max
        return cp.asarray(output)

    def _pool_backward(self, accum_grad):
        accum_grad_col = np.zeros((np.prod(self.pool_shape), accum_grad.size))
        arg_max = self.cache
        accum_grad_col[arg_max, range(accum_grad.size)] = cp.asnumpy(accum_grad)
        return cp.asarray(accum_grad_col)
