from deprecated.metal.nn import NeuralNetwork
import matplotlib.pyplot as plt

class ConvNet(NeuralNetwork):
    """docstring for CovNet."""

    def __init__(self, optimizer, loss, validation_data=None):
        super(ConvNet, self).__init__(optimizer, loss, validation_data=validation_data)

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

    def predict(self, X):
        pred = self._forward_pass(X, training=False)
        list_pred = pred.data.flatten().tolist()
        return list_pred.index(max(list_pred))
