


from typing import Callable
from inspect import signature
import typing

def num_func_args(f: Callable) -> int:
    return len(signature(f).parameters)

def validate_num_args(f: Callable, num_args_required: int):
    num = num_func_args(f)
    if num != num_args_required:
        raise_str = "Function {} got wrong number of arguments, excepted {}, got {}."
        raise TypeError(raise_str.format(f.__name__, num_args_required, num))