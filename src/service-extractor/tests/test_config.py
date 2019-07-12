import pytest

from tests.context import common, extractor
from extractor.config import ExtractorConfig, ExtractorConfigFileNotFoundError


def test_invalid_fpath():
    """Should not be able to initialize `ExtractorConfig` if the config fpath 
    is wrong. Test if `ExtractorConfigFileNotFoundError` is raised.
    """
    with pytest.raises(ExtractorConfigFileNotFoundError):
        ExtractorConfig("conf.yml")
