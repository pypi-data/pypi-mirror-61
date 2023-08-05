from __future__ import print_function, division
from terminaltables import AsciiTable
import cupy as cp
import progressbar
from metalgpu.utils import batch_iterator
from metalgpu.utils.misc import bar_widgets
import matplotlib.pyplot as plt
import numpy as np
class NeuralNetwork(object):
    __slots__ = ('optimizer','layers','errors','loss_function','progressbar','val_set','trainable')
    """Neural Network. Deep Learning base model.
    Parameters:
    -----------
    optimizer: class
        The weight optimizer that will be used to tune the weights in order of minimizing
        the loss.
    loss: class
        Loss function used to measure the model's performance. SquareLoss or CrossEntropy.
    validation: tuple
        A tuple containing validation data and labels (X, y)
    """
    def __init__(self, optimizer, loss, validation_data=None):
        self.optimizer = optimizer
        self.layers = []
        self.errors = {"training": [], "validation": []}
        self.acc = {"training": [], "validation": []}
        self.loss_function = loss
        self.progressbar = progressbar.ProgressBar(widgets=bar_widgets)
        self.val_set = None
        if validation_data:
            X, y = validation_data
            self.val_set = {"X": X, "y": y}

    def set_trainable(self, trainable):
        """ Method which enables freezing of the weights of the network's layers. """
        for layer in self.layers:
            layer.trainable = trainable

    def add(self, layer):
        """ Method which adds a layer to the neural network """
        # If this is not the first layer added then set the input shape
        # to the output shape of the last added layer
        if self.layers:
            layer.set_input_shape(shape=self.layers[-1].output_shape())

        # If the layer has weights that needs to be initialized
        if hasattr(layer, 'load_params'):
            if layer.load_params_ == True:
                layer.load_optimzer(optimizer=self.optimizer)
            else:
                layer

        if hasattr(layer, 'initialize'):
            if layer.load_params_ == False:
                layer.initialize(optimizer=self.optimizer)
            else:
                layer

        # Add layer to the network
        self.layers.append(layer)

    def test_on_batch(self, X, y):
        """ Evaluates the model over a single batch of samples """
        y_pred = self._forward_pass(X, training=False)
        loss = self.loss_function(y, y_pred).loss(training=False)
        acc = self.loss_function(y, y_pred).acc()

        return loss, acc

    def train_on_batch(self, X, y):
        """ Single gradient update over one batch of samples """
        y_pred = self._forward_pass(X, training=True)
        loss = self.loss_function(y, y_pred).loss(training=True)
        acc = self.loss_function(y, y_pred).acc()
        #Calculate the gradient of the loss function wrt y_pred
        loss.sum().backward()
        #Update weights
        self._update_pass()

        return loss.data, acc

    def fit(self, X, y, n_epochs, batch_size):
        """ Trains the model for a fixed number of epochs """
        for _ in self.progressbar(range(n_epochs)):
            batch_acc = []
            batch_error = []
            for X_batch, y_batch in batch_iterator(X, y, batch_size=batch_size):
                loss, acc = self.train_on_batch(X_batch, y_batch)
                batch_error.append(cp.asnumpy(loss))
                batch_acc.append(acc)
                


            self.errors["training"].append(np.mean(batch_error))
            self.acc["training"].append(np.mean(batch_acc))

            if self.val_set is not None:
                val_loss, val_acc = self.test_on_batch(self.val_set["X"], self.val_set["y"])
                self.errors["validation"].append(val_loss.data)
                self.acc["validation"].append(val_acc.data)


        return self.errors["training"], self.errors["validation"]

    def _forward_pass(self, X, training):
        """ Calculate the output of the NN """
        layer_output = X
        for layer in self.layers:
            layer_output = layer.forward_pass(layer_output, training)
        return layer_output

    def _update_pass(self):
        """ Propagate the gradient 'backwards' and update the weights in each layer """
        for layer in reversed(self.layers):
            loss_grad = layer.update_pass()

    def summary(self, name="Model Summary"):
        # Print model name
        print (AsciiTable([[name]]).table)
        # Network input shape (first layer's input shape)
        print ("input Shape: %s" % str(self.layers[0].input_shape))
        # Iterate through network and get each layer's configuration
        table_data = [["Layer Type", "Parameters", "Output Shape"]]
        tot_params = 0
        for layer in self.layers:
            layer_name = layer.layer_name()
            params = layer.parameters_()
            out_shape = layer.output_shape()
            table_data.append([layer_name, str(params), str(out_shape)])
            tot_params += params

        # Print network configuration table
        print (AsciiTable(table_data).table)
        print ("Total Parameters: %d\n" % tot_params)

    def predict(self, X):
        """ Use the trained model to predict labels of X """
        return self._forward_pass(X, training=False)
