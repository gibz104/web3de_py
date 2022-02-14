import time
import functools

# TODO: create "monte carlo timer" decorator that will run function many times and return avg run time


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed_time = end - start
        print(f'Elapsed time ({func.__name__}): {elapsed_time:,} seconds')
        return value
    return wrapper_timer


def timer_ns(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.perf_counter_ns()
        value = func(*args, **kwargs)
        end = time.perf_counter_ns()
        elapsed_time = end - start
        print(f'Elapsed time ({func.__name__}): {elapsed_time:,} nanoseconds')
        return value
    return wrapper_timer
