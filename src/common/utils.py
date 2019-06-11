from datetime import datetime
import functools
import logging

from db.database import IMDb_Database
from imdb.config import AnalyzerConfig
from imdb.ratings import SeriesRatingsCollection

logger = logging.getLogger(__name__)


def timer(in_seconds=False):
    """A decorator that times and prints execution time."""
    def _timer(func):
        @functools.wraps(func)
        def wrapper():
            print("Starting execution...")
            start_time = datetime.now()
            func()
            end_time = datetime.now()
            duration = end_time - start_time
            if in_seconds:
                print("Program runtime: {}.{} secs".format(
                    duration.seconds, duration.microseconds))
            else:
                print("Program runtime: {}".format(duration))
        return wrapper
    return _timer


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


def db_connect(func):
    def wrapper(self, *args, **kwargs):
        with IMDb_Database() as db:
            func(self, db, *args, **kwargs)
    return wrapper
