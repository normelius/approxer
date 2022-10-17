
from typing import Callable
import numpy as np
import numpy.typing as npt
import ctypes
import os
import platform
from numpy.ctypeslib import ndpointer
from inspect import signature

import approxer.exceptions

if platform.uname()[0] == "Windows":
  pass
elif platform.uname()[0] == "Linux":
  pass
else:
  this_dir = os.path.abspath(os.path.dirname(__file__))

callback_funcs = {
  "ode_first_order": ctypes.CFUNCTYPE(None, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_ulong, ctypes.POINTER(ctypes.c_double))
}

class Arguments(ctypes.Structure):
  _fields_ = [
    ("ode", callback_funcs["ode_first_order"]),
    ("y", ctypes.POINTER(ctypes.c_double)),
    ("iterations", ctypes.c_ulong),
    ("ncols", ctypes.c_ulong),
    ("t_0", ctypes.c_double),
    ("t", ctypes.c_double),
    ("t_out", ctypes.POINTER(ctypes.c_double)),
    ("y_out", ctypes.POINTER(ctypes.POINTER(ctypes.c_double))),
  ]
  def __init__(self, ode, y, iterations, ncols, t_0, t, t_out, y_out):
    self.ode = ode
    self.y = np.ctypeslib.as_ctypes(y)
    self.iterations = iterations
    self.t_0 = t_0
    self.t = t
    self.t_out = np.ctypeslib.as_ctypes(t_out)
    self.y_out = y_out.ctypes.data_as(ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))
    self.ncols = ncols

libname = "./ode_solvers.cpython-39-darwin.so"
lib = ctypes.CDLL(os.path.join(this_dir, libname))
lib.euler_lib.argtypes = [ctypes.POINTER(Arguments)]


def euler(f: Callable, y: npt.NDArray[np.float64] = np.array([1.], dtype = np.float64), iterations: int = 1000, t_0: float = 0.0, t: float = 10.0):
  """
  Solves a first-order ordinary differential equation (ODE) using the
  forward Euler method. The equation to solve is given by 
    dy/dt = f(t, y)
  with initial condition y_0 at time t_0.
  Math:
    Euler method is given by: y_{n+1} = y_{n} + h*f(t_{n}, y_{n})
  :param f: This is a user specified function containing signature f(t: float, y: np.array) -> np.array
  :param y: Initial values to be used, specified as an array.
  :param iteration: An integer specifying how many iterations that should be used. Observe that the step size
      is given by (t - t_0) / iterations.
  :param t_0: The starting time value, specified as a float.
  :param t: The final time value, specified as a float.
  """
  approxer.exceptions.validate_num_args(f, 2)
  if y.ndim != 1:
    raise TypeError("Argument 'y' should have ndim = 1, got ndim = {}".format(y.ndim))
  if iterations <= 0:
    raise TypeError("Argument 'iterations' have to be greater than 0.")

  ncols = y.shape[0]
  t_out = np.zeros((iterations + 1), dtype = np.float64)
  y_out = np.zeros(shape = (iterations + 1, ncols), dtype = np.float64)

  def middle_handler(t, y, ncols, y_temp):
    """
    This middle handler is used before the call to the user specified
    ODE. It is used to transform c++ pointers into a numpy array which
    is passed to the user ODE function.
    """
    buf_ctypes = ctypes.cast(y, ctypes.POINTER(ctypes.c_double*ncols))[0]
    buf_np = np.frombuffer(buf_ctypes, np.float64)
    ode_value = f(t, buf_np)
    ctypes.memmove(y_temp, ode_value.ctypes.data, ode_value.nbytes)

  args = Arguments(callback_funcs["ode_first_order"](middle_handler), y, iterations, ncols, t_0, t, t_out, y_out)
  lib.euler_lib(args)
  return t_out, y_out

def f(t, y):
  #delta = 0.02
  #beta = 0.01
  #out = np.empty((2))
  #out[0] = y[0] * (1 - beta * y[1])
  #out[1] = y[1] * (-1 + delta * y[0])
  return y

def main():
  ts, ys = euler(f, y = np.array([1.,]), iterations = 10**5, t_0 = 0, t = 4)
  print(ys)

if __name__ == '__main__':
    main()

