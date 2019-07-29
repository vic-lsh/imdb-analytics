import logging
import logging.config
import pickle
import os
import sys
import yaml

from mongoengine import connect
from pypaca import time

from common.utils import get_logger_cfg_fpath
from extractor import IMDb_Queries_Manager
from extractor.config import ExtractorConfig
from extractor.ratings import SeriesRatingsCollection, SeriesRatings

LOGGER_CONFIG_FPATH = 'config_logger.yml'

try:
    logging.config.fileConfig(get_logger_cfg_fpath())
except FileNotFoundError as e:
    print(e)
logger = logging.getLogger(__name__)


@time.timer
def main():
    config = ExtractorConfig()
    manager = IMDb_Queries_Manager(config)

    if len(sys.argv) > 1:
        manager.add_multiple_queries(sys.argv[1:])
    else:
        manager.add_multiple_queries(config.tv_series_names)

    successful = manager.execute()
    if not successful:
        logger.error("Err: an error has occured during execution.")
    else:
        logger.info("Success!")


if __name__ == "__main__":
    main()