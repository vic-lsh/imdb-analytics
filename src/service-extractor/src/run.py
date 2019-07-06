import logging
import logging.config
import pickle
import os
import sys
import yaml

from mongoengine import connect

from extractor import IMDb_Queries_Manager
from extractor.config import ExtractorConfig
from extractor.ratings import SeriesRatingsCollection, SeriesRatings
from pypaca import time

LOGGER_CONFIG_FPATH = 'config_logger.yml'

if os.path.isfile(LOGGER_CONFIG_FPATH):
    with open(os.path.abspath('config_logger.yml'), 'r') as f:
        cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(cfg)
else:
    print("Warning: logging config file not found.")

logger = logging.getLogger(__name__)


@time.timer
def main():
    config = ExtractorConfig()
    manager = IMDb_Queries_Manager(config)

    if len(sys.argv) > 1:
        manager.add_multiple_queries(sys.argv[1:])
    else:
        manager.add_multiple_queries(config.tv_series_names)

    manager.api_execute()


if __name__ == "__main__":
    main()
