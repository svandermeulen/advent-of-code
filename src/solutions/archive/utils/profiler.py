"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 16/12/2020
"""


import time

from functools import wraps
from typing import Callable


def profile(func: Callable):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        string = "{state} function {input}"
        print(string.format(state="Started", input=f"{func.__name__}"))
        t0 = time.time()
        result = func(*args, **kwargs)
        time_taken = time.time() - t0
        print(string.format(state="Finished", input=f"{func.__name__} after {time_taken:.8f} seconds"))
        return result
    return func_wrapper


def main():
    pass


if __name__ == "__main__":
    main()
