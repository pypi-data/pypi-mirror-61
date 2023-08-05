from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from metal.utils.functions import batch_iterator
from metal.utils.misc import bar_widgets
import progressbar
from metal.learners.solver import Solver

class NeuralNetwork(object):
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
    def __init__(self, optimizer, loss, validation_data=None, layers = []):
        self.optimizer = optimizer
        self.layers = layers
        self.errors = {"training": [], "validation": []}
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
        # If the layer has weights that needs to be initialized
        layer(optimizer=self.optimizer)
        # Add layer to the network
        self.layers.append(layer)

    def test_on_batch(self, X, y):
        """ Single gradient update over one batch of samples """
        y_pred = self._forward_pass(X, retain_derived=False)
        loss = self.loss_function.loss(y, y_pred)
        acc = self.loss_function.acc(y, y_pred)
        return loss, acc


    def train_on_batch(self, X, y):
        """ Single gradient update over one batch of samples """
        y_pred = self._forward_pass(X, retain_derived=True)
        loss = self.loss_function.loss(y, y_pred)
        acc = self.loss_function.acc(y, y_pred)
        gradient = self.loss_function.grad(y, y_pred)
        #Calculate the gradient of the loss function wrt y_pred
        self._backward_pass(loss_grad=gradient)
        #Update weights
        self._update_pass(loss=loss)
        return loss, acc

    def _forward_pass(self, X, retain_derived=True):
        """ Calculate the output of the NN """
        layer_output = X
        for layer in self.layers:
            layer_output = layer.forward(layer_output, retain_derived)

        return layer_output

    def _backward_pass(self, loss_grad):
        """ Propagate the gradient 'backwards' and update the weights in each layer """
        for layer in reversed(self.layers):
            loss_grad = layer.backward(loss_grad)

    def _update_pass(self, loss):
        """ Propagate the gradient 'backwards' and update the weights in each layer """
        for layer in reversed(self.layers):
            layer.update(loss)

    def fit(self, X, y, n_epochs, batch_size):
        """ Trains the model for a fixed number of epochs """
        for _ in self.progressbar(range(n_epochs)):
            batch_error = []
            for X_batch, y_batch in batch_iterator(X, y, batch_size=batch_size):
                loss, acc = self.train_on_batch(X_batch, y_batch)
                batch_error.append(loss)


            self.errors["training"].append(np.mean(batch_error))

            if self.val_set is not None:
                val_loss, val_acc = self.test_on_batch(self.val_set["X"], self.val_set["y"])
                self.errors["validation"].append(val_loss)


        return self.errors["training"], self.errors["validation"]


    def eval(self, X_test, y_test):
        train_err, val_err = self.errors['training'], self.errors["validation"]
        # Training and validation error plot
        n = len(train_err)
        training, = plt.plot(range(n), train_err, label="Training Error")
        validation, = plt.plot(range(n), val_err, label="Validation Error")
        plt.legend(handles=[training, validation])
        plt.title("Error Plot")
        plt.ylabel('Error')
        plt.xlabel('Iterations')
        plt.show()
        _, accuracy = self.test_on_batch(X_test, y_test)
        print ("Accuracy:", accuracy)
        return accuracy

    def predict(self, X):
        pred = self._forward_pass(X, retain_derived=False)
        list_pred = pred.data.flatten().tolist()
        return list_pred.index(max(list_pred))

    def with_solver(self,data,**kwargs):
        self.solver = Solver(self,data,**kwargs)
