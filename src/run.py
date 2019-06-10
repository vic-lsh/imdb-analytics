import logging
import logging.config
import pickle
import os
import yaml

from imdb.analyzer import IMDb_Queries_Manager
from imdb.config import AnalyzerConfig
from imdb.ratings import SeriesRatingsCollection
from common.utils import timer

with open('config_logger.yml', 'r') as f:
    cfg = yaml.safe_load(f.read())
logging.config.dictConfig(cfg)

logger = logging.getLogger(__name__)


@timer(in_seconds=True)
def main():
    config = AnalyzerConfig()
    manager = IMDb_Queries_Manager(config)
    manager.add_multiple_queries(config.tv_series_names)
    print(manager.pending_queries)
    manager.execute()


if __name__ == "__main__":
    main()
