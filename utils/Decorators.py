import time
import functools
import numpy as np


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed_time = end - start
        print(f'Elapsed time ({func.__name__}): {elapsed_time:,.5f} seconds')
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


def mc_timer(count: int = 100):
    def decorator(func):
        @functools.wraps(func)
        def mc_timer_wrapper(*args, **kwargs):
            runtimes = []
            for i in range(count):
                start = time.perf_counter()
                func(*args, **kwargs)
                end = time.perf_counter()
                elapsed_time = end - start
                runtimes.append(elapsed_time)
            avg_runtime = np.mean(runtimes)
            sd = np.std(runtimes)
            print(f'Average elapsed time ({count:,} runs): {avg_runtime:,.5f} seconds ± {sd:,.5f}')
        return mc_timer_wrapper
    return decorator
