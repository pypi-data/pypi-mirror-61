from copy import deepcopy
from abc import ABC, abstractmethod
import numpy as np
from math import erf
from metal.utils.functions import gaussian_cdf


class SchedulerBase(ABC):
    def __init__(self):
        """Abstract base class for all Scheduler objects."""
        self.hyperparameters = {}

    def __call__(self, step=None, cur_loss=None):
        return self.learning_rate(step=step, cur_loss=cur_loss)

    def copy(self):
        """Return a copy of the current object."""
        return deepcopy(self)

    def set_params(self, hparam_dict):
        """Set the scheduler hyperparameters from a dictionary."""
        if hparam_dict is not None:
            for k, v in hparam_dict.items():
                if k in self.hyperparameters:
                    self.hyperparameters[k] = v
        return self

    @abstractmethod
    def learning_rate(self, step=None):
        raise NotImplementedError


class ConstantScheduler(SchedulerBase):
    def __init__(self, lr=0.01, **kwargs):
        """
        Returns a fixed learning rate, regardless of the current step.
        Parameters
        ----------
        initial_lr : float
            The learning rate. Default is 0.01
        """
        super().__init__()
        self.lr = lr
        self.hyperparameters = {"id": "ConstantScheduler", "lr": self.lr}

    def __str__(self):
        return "ConstantScheduler(lr={})".format(self.lr)

    def learning_rate(self, **kwargs):
        """
        Return the current learning rate.
        Returns
        -------
        lr : float
            The learning rate
        """
        return self.lr
