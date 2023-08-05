import numpy as np
from metal.utils.functions import accuracy_score


class Loss(object):
    def loss(self, y_true, y_pred):
        return NotImplementedError()

    def gradient(self, y, y_pred):
        raise NotImplementedError()

    def acc(self, y, y_pred):
        return 0



class SquareLoss(Loss):
    def __init__(self): pass

    def loss(self, y, y_pred):
        return 0.5 * np.power((y - y_pred), 2)

    def gradient(self, y, y_pred):
        return -(y - y_pred)



class CrossEntropy(Loss):
    def __init__(self): pass

    def loss(self, y, p):
        # Avoid division by zero
        eps = np.finfo(np.float32).eps
        return np.mean(- y * np.log(p+eps) - (1 - y) * np.log((1 - p)+eps))

    def acc(self, y, p):
        return accuracy_score(np.argmax(y, axis=1), np.argmax(p, axis=1))

    def grad(self, y, p):
        # Avoid division by zero
        eps = np.finfo(np.float32).eps
        return - (y / p+eps) + (1 - y) / (1 - p+eps)
