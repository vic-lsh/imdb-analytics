import logging
import pickle
import os

from analyzer import IMDb_Queries_Manager
from config import AnalyzerConfig
from ratings import SeriesRatingsCollection
from utils import timer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)

handler.setFormatter(formatter)
logger.addHandler(handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@timer(in_seconds=True)
def main():
    config = AnalyzerConfig()
    manager = IMDb_Queries_Manager(config)
    manager.add_multiple_queries(config.tv_series_names)
    print(manager.pending_queries)
    manager.execute()


if __name__ == "__main__":
    main()
