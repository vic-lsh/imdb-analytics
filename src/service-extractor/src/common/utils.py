"""
common/utils.py
---------------

Contains project-wide utility functions.
"""

import os


def get_logger_cfg_fpath() -> str:
    """Returns the absolute path to logger config"""
    return ''.join([os.getcwd(), '/cfg/logger_cfg.ini'])
