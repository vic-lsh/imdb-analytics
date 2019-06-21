from datetime import datetime
import functools
import logging

from crawler.config import AnalyzerConfig
from crawler.ratings import SeriesRatingsCollection

logger = logging.getLogger(__name__)


def timer(func):
    """A decorator that times and prints execution time."""
    def timer_wrapper(*args, **kwargs):
        start_time = datetime.now()
        resp = func(*args, **kwargs)
        end_time = datetime.now()
        duration = end_time - start_time
        print("{:<40} runtime: {}.{} secs".format(
            func.__name__, duration.seconds, duration.microseconds))
        return resp
    return timer_wrapper


def timeout(delay, ExceptionType=Exception):
    def _timeout(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            start = datetime.now()
            while True:
                try:
                    ret = func(self, *args, **kwargs)
                except ExceptionType:
                    continue
                finally:
                    now = datetime.now()
                    if (now - start).seconds > delay:
                        raise TimeoutError
                        break
            return ret
        return wrapper
    return _timeout
