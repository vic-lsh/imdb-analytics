"""
common/utils.py
---------------

Contains project-wide utility functions.
"""

import logging
import logging.config
import os


def get_logger_cfg_fpath() -> str:
    """Returns the absolute path to logger config"""
    return ''.join([os.getcwd(), '/cfg/logger_cfg.ini'])


def make_logger(logger_name: str) -> logging.Logger:
    """Makes a logger.

    Defaults to using settings defined in the logger config file.
    If logging config file cannot be loaded, default to:

        - Formatting: time, name, levelname, msg
        - Level: Debug
    """
    logger = logging.getLogger(logger_name)
    try:
        logging.config.fileConfig(get_logger_cfg_fpath())
    except FileNotFoundError as e:
        print(e)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
