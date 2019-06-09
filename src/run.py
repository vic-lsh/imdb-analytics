from analyzer import IMDb_Analyzer
from config import AnalyzerConfig
from utils import timer


@timer(in_seconds=True)
def main():
    config = AnalyzerConfig()
    analyzer = IMDb_Analyzer(config)
    for tv_series in config.tv_series_names:
        ratings = analyzer.query(tv_series)
        print(ratings)


if __name__ == "__main__":
    main()
