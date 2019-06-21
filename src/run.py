import logging
import logging.config
import pickle
import os
from os.path import abspath
import yaml

from mongoengine import connect

from crawler.analyzer import IMDb_Queries_Manager
from crawler.config import AnalyzerConfig
from crawler.ratings import SeriesRatingsCollection, SeriesRatings
from common.utils import timer

with open(abspath('src/config_logger.yml'), 'r') as f:
    cfg = yaml.safe_load(f.read())
logging.config.dictConfig(cfg)

logger = logging.getLogger(__name__)


@timer
def main():
    config = AnalyzerConfig()
    manager = IMDb_Queries_Manager(config)
    manager.add_multiple_queries(config.tv_series_names)
    manager.api_execute()


if __name__ == "__main__":
    main()
