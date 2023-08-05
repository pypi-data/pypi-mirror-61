from __future__ import print_function, division
from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
import os
import pickle as pickle
import numpy as np
from metal.optimizers import optimizer as optim
from metal.utils.functions import accuracy_score

#from cs321


"""
A Solver encapsulates all the logic necessary for training classification
models. The Solver performs stochastic gradient descent using different
update rules defined in optim.py.
The solver accepts both training and validataion data and labels so it can
periodically check classification accuracy on both training and validation
data to watch out for overfitting.
To train a model, you will first construct a Solver instance, passing the
model, dataset, and various options (learning rate, batch size, etc) to the
constructor. You will then call the train() method to run the optimization
procedure and train the model.
After the train() method returns, model.params will contain the parameters
that performed best on the validation set over the course of training.
In addition, the instance variable solver.loss_history will contain a list
of all losses encountered during training and the instance variables
solver.train_acc_history and solver.val_acc_history will be lists of the
accuracies of the model on the training and validation set at each epoch.
Example usage might look something like this:
data = {
  'X_train': # training data
  'y_train': # training labels
  'X_val': # validation data
  'y_val': # validation labels
}
model = MyAwesomeModel(hidden_size=100, reg=10)
solver = Solver(model, data,
                update_rule='sgd',
                optim_config={
                  'learning_rate': 1e-3,
                },
                lr_decay=0.95,
                num_epochs=10, batch_size=100,
                print_every=100)
solver.train()
A Solver works on a model object that must conform to the following API:
- model.params must be a dictionary mapping string parameter names to numpy
  arrays containing parameter values.
- model.loss(X, y) must be a function that computes training-time loss and
  gradients, and test-time classification scores, with the following inputs
  and outputs:
  Inputs:
  - X: Array giving a minibatch of input data of shape (N, d_1, ..., d_k)
  - y: Array of labels, of shape (N,) giving labels for X where y[i] is the
    label for X[i].
  Returns:
  If y is None, run a test-time forward pass and return:
  - scores: Array of shape (N, C) giving classification scores for X where
    scores[i, c] gives the score of class c for X[i].
  If y is not None, run a training time forward and backward pass and
  return a tuple of:
  - loss: Scalar giving the loss
  - grads: Dictionary with the same keys as self.params mapping parameter
    names to gradients of the loss with respect to those parameters.
"""

"""
Construct a new Solver instance.
Required arguments:
- model: A model object conforming to the API described above
- data: A dictionary of training and validation data containing:
  'X_train': Array, shape (N_train, d_1, ..., d_k) of training images
  'X_val': Array, shape (N_val, d_1, ..., d_k) of validation images
  'y_train': Array, shape (N_train,) of labels for training images
  'y_val': Array, shape (N_val,) of labels for validation images
Optional arguments:
- update_rule: A string giving the name of an update rule in optim.py.
  Default is 'sgd'.
- optim_config: A dictionary containing hyperparameters that will be
  passed to the chosen update rule. Each update rule requires different
  hyperparameters (see optim.py) but all update rules require a
  'learning_rate' parameter so that should always be present.
- lr_decay: A scalar for learning rate decay; after each epoch the
  learning rate is multiplied by this value.
- batch_size: Size of minibatches used to compute loss and gradient
  during training.
- num_epochs: The number of epochs to run for during training.
- print_every: Integer; training losses will be printed every
  print_every iterations.
- verbose: Boolean; if set to false then no output will be printed
  during training.
- num_train_samples: Number of training samples used to check training
  accuracy; default is 1000; set to None to use entire training set.
- num_val_samples: Number of validation samples to use to check val
  accuracy; default is None, which uses the entire validation set.
- checkpoint_name: If not None, then save model checkpoints here every
  epoch.
"""


class Solver(object):

    def __init__(self, model, data, **kwargs):

        self.layers = model.layers
        self.loss_function = model.loss_function

        self.X_train = data['X_train']
        self.y_train = data['y_train']
        self.X_val = data['X_val']
        self.y_val = data['y_val']


        # Unpack keyword arguments
        self.update_rule = kwargs.pop('update_rule', 'sgd')
        self.optim_config = kwargs.pop('optim_config', {'learning_rate':1e-3})
        self.lr_decay = kwargs.pop('lr_decay', 1.0)
        self.batch_size = kwargs.pop('batch_size', 100)
        self.num_epochs = kwargs.pop('num_epochs', 10)
        self.num_train_samples = kwargs.pop('num_train_samples', 1000)
        self.num_val_samples = kwargs.pop('num_val_samples', None)

        self.checkpoint_name = kwargs.pop('checkpoint_name', None)
        self.print_every = kwargs.pop('print_every', 10)
        self.verbose = kwargs.pop('verbose', True)

        # Throw an error if there are extra keyword arguments
        if len(kwargs) > 0:
            extra = ', '.join('"%s"' % k for k in list(kwargs.keys()))
            raise ValueError('Unrecognized arguments %s' % extra)

        # Make sure the update rule exists, then replace the string
        # name with the actual function
        if not hasattr(optim, self.update_rule):
            raise ValueError('Invalid update_rule "%s"' % self.update_rule)
        self.update_rule = getattr(optim, self.update_rule)

        self._init_optimizer()
        self._reset()

    def _init_optimizer(self):
        for l in self.layers:
            l.change_optimizer(self.update_rule(lr = self.optim_config['learning_rate']))

    def _reset(self):
        #Set up some book-keeping variables for optimization. Don't call this
        #manually.

        # Set up some variables for book-keeping
        self.epoch = 0
        self.best_val_acc = 0
        self.best_params = {}
        self.loss_history = []
        self.train_acc_history = []
        self.val_acc_history = []

    def _step(self):

        #Make a single gradient update. This is called by train() and should not
        #be called manually.

        # Make a minibatch of training data
        num_train = self.X_train.shape[0]
        batch_mask = np.random.choice(num_train, self.batch_size)
        X_batch = self.X_train[batch_mask]
        y_batch = self.y_train[batch_mask]

        # Compute loss and gradient
        loss, _ = self.train_on_batch(X_batch, y_batch)
        self.loss_history.append(loss)

    def check_accuracy(self, X, y, num_samples=None, batch_size=100):
        """
        Check accuracy of the model on the provided data.
        Inputs:
        - X: Array of data, of shape (N, d_1, ..., d_k)
        - y: Array of labels, of shape (N,)
        - num_samples: If not None, subsample the data and only test the model
          on num_samples datapoints.
        - batch_size: Split X and y into batches of this size to avoid using
          too much memory.
        Returns:
        - acc: Scalar giving the fraction of instances that were correctly
          classified by the model.
        """

        # Maybe subsample the data
        N = X.shape[0]
        if num_samples is not None and N > num_samples:
            mask = np.random.choice(N, num_samples)
            N = num_samples
            X = X[mask]
            y = y[mask]

        # Compute predictions in batches
        num_batches = N // batch_size
        if N % batch_size != 0:
            num_batches += 1
        y_pred = []
        for i in range(num_batches):
            start = i * batch_size
            end = (i + 1) * batch_size
            scores = self._forward_pass(X[start:end],retain_derived=False)
            y_pred.append(np.argmax(scores, axis=1))
        y_pred = np.hstack(y_pred)
        return accuracy_score(np.argmax(y, axis=1), y_pred)

    def train(self):
        """
        Run optimization to train the model.
        """
        num_train = self.X_train.shape[0]
        iterations_per_epoch = max(num_train // self.batch_size, 1)
        num_iterations = self.num_epochs * iterations_per_epoch

        for t in range(num_iterations):
            self._step()

            # Maybe print training loss
            if self.verbose and t % self.print_every == 0:
                print('(Iteration %d / %d) loss: %f' % (
                       t + 1, num_iterations, self.loss_history[-1]))

            # At the end of every epoch, increment the epoch counter and decay
            # the learning rate.
            epoch_end = (t + 1) % iterations_per_epoch == 0
            if epoch_end:
                self.epoch += 1

            # Check train and val accuracy on the first iteration, the last
            # iteration, and at the end of each epoch.
            first_it = (t == 0)
            last_it = (t == num_iterations - 1)
            if first_it or last_it or epoch_end:
                train_acc = self.check_accuracy(self.X_train, self.y_train,
                    num_samples=self.num_train_samples)
                val_acc = self.check_accuracy(self.X_val, self.y_val,
                    num_samples=self.num_val_samples)
                self.train_acc_history.append(train_acc)
                self.val_acc_history.append(val_acc)
                #self._save_checkpoint()

                if self.verbose:
                    print('(Epoch %d / %d) train acc: %f; val_acc: %f' % (
                           self.epoch, self.num_epochs, train_acc, val_acc))

                # Keep track of the best model
                    if val_acc > self.best_val_acc:
                        self.best_val_acc = val_acc
                        self.best_params = {}

                        for c,l in enumerate(self.layers):
                            if "W" and "b" in l.parameters:
                                for k, v in l.parameters.items():
                                    self.best_params[k+str(c+1)] = v.copy()

        for c,l in  enumerate(self.layers):
            if "W" and "b" in l.parameters:
                for k, v in l.parameters.items():
                    l.parameters[k]=self.best_params[k+str(c+1)]


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
