
import numpy as np
import unittest

import approxer 

class TestEuler(unittest.TestCase):
  def test_euler_1(self):
    def f(t, y):
      return y

    c = np.exp(4)
    ts, ys = approxer.euler(f, y = np.array([1.]), iterations = 10**4, t = 4)
    np.testing.assert_almost_equal(c, ys[-1], 1)

  def test_euler_2(self):
    def f(t, y):
      return np.array([-2*y + 2 - np.exp(-4*t)])
    
    t = 2
    correct = 0.5 * (np.exp(-4*t) - np.exp(-2*t) + 2)
    ts, ys = approxer.euler(f, y = np.array([1.]), iterations = 10**4, t = t)
    np.testing.assert_almost_equal(correct, ys[-1], 4)

if __name__ == '__main__':
  unittest.main()

