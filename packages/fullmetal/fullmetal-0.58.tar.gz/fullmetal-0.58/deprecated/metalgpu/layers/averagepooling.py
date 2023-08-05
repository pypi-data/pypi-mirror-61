import cupy as cp
from metalgpu.layers.layer import PoolingLayer

class AveragePooling2D(PoolingLayer):
    def _pool_forward(self, X_col):
        output = cp.mean(X_col, axis=0)
        return output

    def _pool_backward(self, accum_grad):
        accum_grad_col = cp.zeros((cp.prod(self.pool_shape), accum_grad.size))
        accum_grad_col[:, range(accum_grad.size)] = 1. / accum_grad_col.shape[0] * accum_grad
        return accum_grad_col
