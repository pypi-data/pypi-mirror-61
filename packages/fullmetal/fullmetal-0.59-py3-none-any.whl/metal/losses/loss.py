import numpy as np
from metal.utils.functions import accuracy_score,  is_binary, is_stochastic
from abc import ABC, abstractmethod


class ObjectiveBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def loss(self, y_true, y_pred):
        pass

    @abstractmethod
    def grad(self, y_true, y_pred, **kwargs):
        pass


class CrossEntropy(ObjectiveBase):
    def __init__(self):
        """
        A cross-entropy loss.
        Notes
        -----
        For a one-hot target **y** and predicted class probabilities
        :math:`\hat{\mathbf{y}}`, the cross entropy is
        .. math::
                \mathcal{L}(\mathbf{y}, \hat{\mathbf{y}})
                    = \sum_i y_i \log \hat{y}_i
        """
        super().__init__()

    def __call__(self, y, y_pred):
        return self.loss(y, y_pred)

    def __str__(self):
        return "CrossEntropy"

    @staticmethod
    def loss(y, y_pred):
        """
        Compute the cross-entropy (log) loss.
        Notes
        -----
        This method returns the sum (not the average!) of the losses for each
        sample.
        Parameters
        ----------
        y : :py:class:`ndarray <numpy.ndarray>` of shape (n, m)
            Class labels (one-hot with `m` possible classes) for each of `n`
            examples.
        y_pred : :py:class:`ndarray <numpy.ndarray>` of shape (n, m)
            Probabilities of each of `m` classes for the `n` examples in the
            batch.
        Returns
        -------
        loss : float
            The sum of the cross-entropy across classes and examples.
        """
        is_binary(y)
        is_stochastic(y_pred)

        # prevent taking the log of 0
        eps = np.finfo(float).eps

        # each example is associated with a single class; sum the negative log
        # probability of the correct label over all samples in the batch.
        # observe that we are taking advantage of the fact that y is one-hot
        # encoded
        cross_entropy = -np.sum(y * np.log(y_pred + eps))
        return cross_entropy

    @staticmethod
    def grad(y, y_pred):
        """
        Compute the gradient of the cross entropy loss with regard to the
        softmax input, `z`.
        Notes
        -----
        The gradient for this method goes through both the cross-entropy loss
        AND the softmax non-linearity to return :math:`\\frac{\partial
        \mathcal{L}}{\partial \mathbf{z}}` (rather than :math:`\\frac{\partial
        \mathcal{L}}{\partial \\text{softmax}(\mathbf{z})}`).
        In particular, let:
        .. math::
            \mathcal{L}(\mathbf{z})
                = \\text{cross_entropy}(\\text{softmax}(\mathbf{z})).
        The current method computes:
        .. math::
            \\frac{\partial \mathcal{L}}{\partial \mathbf{z}}
                &= \\text{softmax}(\mathbf{z}) - \mathbf{y} \\\\
                &=  \hat{\mathbf{y}} - \mathbf{y}
        Parameters
        ----------
        y : :py:class:`ndarray <numpy.ndarray>` of shape `(n, m)`
            A one-hot encoding of the true class labels. Each row constitues a
            training example, and each column is a different class.
        y_pred: :py:class:`ndarray <numpy.ndarray>` of shape `(n, m)`
            The network predictions for the probability of each of `m` class
            labels on each of `n` examples in a batch.
        Returns
        -------
        grad : :py:class:`ndarray <numpy.ndarray>` of shape (n, m)
            The gradient of the cross-entropy loss with respect to the *input*
            to the softmax function.
        """
        is_binary(y)
        is_stochastic(y_pred)

        # derivative of xe wrt z is y_pred - y_true, hence we can just
        # subtract 1 from the probability of the correct class labels
        grad = y_pred - y

        # [optional] scale the gradients by the number of examples in the batch
        # n, m = y.shape
        # grad /= n
        return grad
