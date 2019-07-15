import pytest

from tests.context import extractor
from extractor.config import ExtractorConfig, ExtractorConfigFileNotFoundError


def test_invalid_fpath():
    """Should not be able to initialize `ExtractorConfig` if the config fpath 
    is wrong. Test if `ExtractorConfigFileNotFoundError` is raised.
    """
    invalid_fpath = "conf.yml"
    with pytest.raises(ExtractorConfigFileNotFoundError):
        ExtractorConfig(invalid_fpath)
