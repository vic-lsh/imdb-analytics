import logging
import logging.config
import pickle
import os
from os.path import abspath
import yaml

from mongoengine import connect

from db.models import TVSeries, SeasonRatings, EpisodeRating
from imdb.analyzer import IMDb_Queries_Manager
from imdb.config import AnalyzerConfig
from imdb.ratings import SeriesRatingsCollection, SeriesRatings
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
    manager.db_execute()


if __name__ == "__main__":
    main()
