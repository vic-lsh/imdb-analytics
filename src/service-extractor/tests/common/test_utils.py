import pytest

import os

from tests.context import common
from common import utils


def test_get_logger_cfg_fpath():
    """Tests that the logger config file path returned leads to an actual file
    """
    assert os.path.isfile(utils.get_logger_cfg_fpath())