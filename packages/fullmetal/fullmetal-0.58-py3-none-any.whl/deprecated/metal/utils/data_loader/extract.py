import torch
import torchvision.models as models
import numpy as np

class Detach_params(object):
    """docstring for Detach_params."""

    def __init__(self, model=None):
        super(Detach_params, self).__init__()
        self.model = model
        self.modelparams = {}
        self.modelfeatures = {}

    def show_model(self):
        print(self.model)

    def detach_params(self):
        for name, param in self.model.named_parameters():
            self.modelparams[str(name)] = param.detach().numpy().astype("float32")

    def save_params(self, path, name):
        np.save(path+name, self.modelparams)

    def load_params(self, path, name):
        return np.load(path+name,allow_pickle=True)

    def detach_features(self):
        for name, param in self.model.features.named_parameters():
            self.modelparams[str(name)] = param.detach().numpy().astype("float32")
