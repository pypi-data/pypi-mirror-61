import numbers
import numpy as np

# numpy-ml/numpy_ml/utils/testing.py/

#######################################################################
#                           Data Generators                           #
#######################################################################


def random_one_hot_matrix(n_examples, n_classes):
    """Create a random one-hot matrix of shape (`n_examples`, `n_classes`)"""
    X = np.eye(n_classes)
    X = X[np.random.choice(n_classes, n_examples)]
    return X


def random_stochastic_matrix(n_examples, n_classes):
    """Create a random stochastic matrix of shape (`n_examples`, `n_classes`)"""
    X = np.random.rand(n_examples, n_classes)
    X /= X.sum(axis=1, keepdims=True)
    return X


def random_tensor(shape, standardize=False):
    """
    Create a random real-valued tensor of shape `shape`. If `standardize` is
    True, ensure each column has mean 0 and std 1.
    """
    offset = np.random.randint(-300, 300, shape)
    X = np.random.rand(*shape) + offset

    if standardize:
        eps = np.finfo(float).eps
        X = (X - X.mean(axis=0)) / (X.std(axis=0) + eps)
    return X



def gaussian_cdf(x, mean, var):
    """
    Compute the probability that a random draw from a 1D Gaussian with mean
    `mean` and variance `var` is less than or equal to `x`.
    """
    eps = np.finfo(float).eps
    x_scaled = (x - mean) / np.sqrt(var + eps)
    return (1 + erf(x_scaled / np.sqrt(2))) / 2


#######################################################################
#                             Assertions                              #
#######################################################################


def is_symmetric(X):
    """Check that an array `X` is symmetric along its main diagonal"""
    return np.allclose(X, X.T)


def is_symmetric_positive_definite(X):
    """
    Check that a matrix `X` is a symmetric and positive-definite.
    """
    if is_symmetric(X):
        try:
            # if matrix is symmetric, check whether the Cholesky decomposition
            # (defined only for symmetric/Hermitian positive definite matrices)
            # exists
            np.linalg.cholesky(X)
            return True
        except np.linalg.LinAlgError:
            return False
    return False


def is_stochastic(X):
    """True if `X` contains probabilities that sum to 1 along the columns"""
    msg = "Array should be stochastic along the columns"
    assert len(X[X < 0]) == len(X[X > 1]) == 0, msg
    assert np.allclose(np.sum(X, axis=1), np.ones(X.shape[0])), msg
    return True


def is_number(a):
    """Check that a value `a` is numeric"""
    return isinstance(a, numbers.Number)


def is_one_hot(x):
    """Return True if array `x` is a binary array with a single 1"""
    msg = "Matrix should be one-hot binary"
    assert np.array_equal(x, x.astype(bool)), msg
    assert np.allclose(np.sum(x, axis=1), np.ones(x.shape[0])), msg
    return True


def is_binary(x):
    """Return True if array `x` consists only of binary values"""
    msg = "Matrix must be binary"
    assert np.array_equal(x, x.astype(bool)), msg
    return True

def random_one_hot_matrix(n_examples, n_classes):
    """Create a random one-hot matrix of shape (`n_examples`, `n_classes`)"""
    X = np.eye(n_classes)
    X = X[np.random.choice(n_classes, n_examples)]
    return X

#######################################################################
#                          functions Metal                            #
#######################################################################


#######################################################################
#                           ML-scratch                                #
#######################################################################
def accuracy_score(y_true, y_pred):
    """ Compare y_true to y_pred and return the accuracy """
    accuracy = np.sum(y_true == y_pred, axis=0) / len(y_true)
    return accuracy


def batch_iterator(X, y=None, batch_size=64):
    """ Simple batch generator """
    n_samples = X.shape[0]
    for i in np.arange(0, n_samples, batch_size):
        begin, end = i, min(i+batch_size, n_samples)
        if y is not None:
            yield X[begin:end], y[begin:end]
        else:
            yield X[begin:end]

def to_categorical(x, n_col=None):
    """ One-hot encoding of nominal values """
    if not n_col:
        n_col = np.amax(x) + 1
    one_hot = np.zeros((x.shape[0], n_col))
    one_hot[np.arange(x.shape[0]), x] = 1
    return one_hot
