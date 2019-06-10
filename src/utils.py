from datetime import datetime
import functools
import logging
import os
import pickle

from config import AnalyzerConfig
from ratings import SeriesRatingsCollection

logger = logging.getLogger(__name__)


def timer(in_seconds=False):
    """A decorator that times and prints execution time."""
    def _timer(func):
        @functools.wraps(func)
        def wrapper():
            logger.info("Starting execution...")
            start_time = datetime.now()
            func()
            end_time = datetime.now()
            duration = end_time - start_time
            if in_seconds:
                logger.info("Program runtime: {}.{} secs".format(
                    duration.seconds, duration.microseconds))
            else:
                logger.info("Program runtime: {}".format(duration))
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


def serialize_ratings_if_configured(config: AnalyzerConfig):
    def _serialize(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if config.should_serialize and \
                    os.path.isfile(config.serialization_filename):
                with open(config.serialization_filename, 'rb') as pkl:
                    ratings_collection = pickle.load(pkl)
            else:
                ratings_collection = SeriesRatingsCollection()

            args[0] = ratings_collection
            func(*args, **kwargs)

            if config.should_serialize:
                with open(config.serialization_filename, 'w+b') as pkl:
                    pickle.dump(ratings_collection, pkl)
        return wrapper
    return _serialize
