import logging

from analyzer import IMDb_Analyzer
from config import AnalyzerConfig
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
    for tv_series in config.tv_series_names:
        ratings = analyzer.query(tv_series)
        print(ratings)


if __name__ == "__main__":
    main()
