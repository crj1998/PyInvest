import time
import functools

def retry(max_trials=3, interval=None):
    """ failure retry. 
    @retry()
    def f():
        ...
    """
    assert isinstance(max_trials, int) and max_trials>0
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret = None
            nonlocal max_trials
            while ret is None and max_trials > 0:
                ret = func(*args, **kwargs)
                max_trials -= 1
                # print(f'func {func.__name__} {max_trials} retry left.')
                if ret is None and max_trials > 0 and isinstance(interval, (float, int)): time.sleep(interval)
            return ret
        return wrapper
    return decorator
