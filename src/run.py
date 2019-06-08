from analyzer import IMDb_Analyzer
from utils import timer


@timer(in_seconds=True)
def main():
    analyzer = IMDb_Analyzer()
    analyzer.query("Game of Thrones")


if __name__ == "__main__":
    main()
