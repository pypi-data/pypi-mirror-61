import numpy as np
import re
from metal.schedulers.scheduler import SchedulerBase, ConstantScheduler


class SchedulerInitializer(object):
    def __init__(self, param=None, lr=None):
        """
        A class for initializing learning rate schedulers. Valid inputs are:
            (a) __str__ representations of `SchedulerBase` instances
            (b) `SchedulerBase` instances
            (c) Parameter dicts (e.g., as produced via the `summary` method in
                `LayerBase` instances)
        If `param` is `None`, return the ConstantScheduler with learning rate
        equal to `lr`.
        """
        if all([lr is None, param is None]):
            raise ValueError("lr and param cannot both be `None`")

        self.lr = lr
        self.param = param

    def __call__(self):
        param = self.param
        if param is None:
            scheduler = ConstantScheduler(self.lr)
        elif isinstance(param, SchedulerBase):
            scheduler = param
        elif isinstance(param, str):
            scheduler = self.init_from_str()
        elif isinstance(param, dict):
            scheduler = self.init_from_dict()
        return scheduler

    def init_from_str(self):
        r = r"([a-zA-Z]*)=([^,)]*)"
        sch_str = self.param.lower()
        kwargs = dict([(i, eval(j)) for (i, j) in re.findall(r, sch_str)])

        if "constant" in sch_str:
            scheduler = ConstantScheduler(**kwargs)
        elif "exponential" in sch_str:
            scheduler = ExponentialScheduler(**kwargs)
        elif "noam" in sch_str:
            scheduler = NoamScheduler(**kwargs)
        elif "king" in sch_str:
            scheduler = KingScheduler(**kwargs)
        else:
            raise NotImplementedError("{}".format(sch_str))
        return scheduler

    def init_from_dict(self):
        S = self.param
        sc = S["hyperparameters"] if "hyperparameters" in S else None

        if sc is None:
            raise ValueError("Must have `hyperparameters` key: {}".format(S))

        if sc and sc["id"] == "ConstantScheduler":
            scheduler = ConstantScheduler().set_params(sc)
        elif sc and sc["id"] == "ExponentialScheduler":
            scheduler = ExponentialScheduler().set_params(sc)
        elif sc and sc["id"] == "NoamScheduler":
            scheduler = NoamScheduler().set_params(sc)
        elif sc:
            raise NotImplementedError("{}".format(sc["id"]))
        return scheduler
