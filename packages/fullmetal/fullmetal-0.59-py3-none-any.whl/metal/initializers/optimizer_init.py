import numpy as np
import re
from metal.optimizers.optimizer  import OptimizerBase, Adam, SGD


class OptimizerInitializer(object):
    def __init__(self, param=None):
        """
        A class for initializing optimizers. Valid inputs are:
            (a) __str__ representations of `OptimizerBase` instances
            (b) `OptimizerBase` instances
            (c) Parameter dicts (e.g., as produced via the `summary` method in
                `LayerBase` instances)
        If `param` is `None`, return the SGD optimizer with default parameters.
        """
        self.param = param

    def __call__(self):
        param = self.param
        if param is None:
            opt = SGD()
        elif isinstance(param, OptimizerBase):
            opt = param
        elif isinstance(param, str):
            opt = self.init_from_str()
        elif isinstance(param, dict):
            opt = self.init_from_dict()
        return opt

    def init_from_str(self):
        r = r"([a-zA-Z]*)=([^,)]*)"
        opt_str = self.param.lower()
        kwargs = dict([(i, eval(j)) for (i, j) in re.findall(r, opt_str)])
        if "sgd" in opt_str:
            optimizer = SGD(**kwargs)
        elif "adagrad" in opt_str:
            optimizer = AdaGrad(**kwargs)
        elif "rmsprop" in opt_str:
            optimizer = RMSProp(**kwargs)
        elif "adam" in opt_str:
            optimizer = Adam(**kwargs)
        else:
            raise NotImplementedError("{}".format(opt_str))
        return optimizer

    def init_from_dict(self):
        O = self.param
        cc = O["cache"] if "cache" in O else None
        op = O["hyperparameters"] if "hyperparameters" in O else None

        if op is None:
            raise ValueError("Must have `hyperparemeters` key: {}".format(O))

        if op and op["id"] == "SGD":
            optimizer = SGD().set_params(op, cc)
        elif op and op["id"] == "RMSProp":
            optimizer = RMSProp().set_params(op, cc)
        elif op and op["id"] == "AdaGrad":
            optimizer = AdaGrad().set_params(op, cc)
        elif op and op["id"] == "Adam":
            optimizer = Adam().set_params(op, cc)
        elif op:
            raise NotImplementedError("{}".format(op["id"]))
        return optimizer
