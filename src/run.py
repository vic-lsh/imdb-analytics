import logging
import pickle
import os

from analyzer import IMDb_Analyzer
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
    analyzer = IMDb_Analyzer(config)

    if config.should_serialize and \
            os.path.isfile(config.serialization_filename):
        with open(config.serialization_filename, 'rb') as pkl:
            ratings_collection = pickle.load(pkl)
    else:
        ratings_collection = SeriesRatingsCollection()

    for tv_series in config.tv_series_names:
        if tv_series not in ratings_collection:
            ratings = analyzer.query(tv_series)
            ratings_collection.add(ratings)

    # print(ratings_collection)

    if config.should_serialize:
        with open(config.serialization_filename, 'w+b') as pkl:
            pickle.dump(ratings_collection, pkl)


if __name__ == "__main__":
    main()
