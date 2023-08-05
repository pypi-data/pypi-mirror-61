import numpy as np
from metal.layers.flatten import Flatten
import unittest


truefl = np.array([[ 1.62434536, -0.61175641, -0.52817175, -1.07296862,  0.86540763, -2.3015387,
   1.74481176, -0.7612069, ]])

class flattentest(unittest.TestCase):
    def testflatten(self):
        f = Flatten()
        np.random.seed(1)
        in_=np.random.randn(1,2,2,2)
        out=f.forward(in_)
        assert out.shape,(in_.shape[0]==in_.shape[1]*in_.shape[2]*in_.shape[3])
        assert np.allclose(out , truefl)
