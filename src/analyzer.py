import functools
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from constants import IMDb_Constants as consts
from series_ratings import SeriesRatings


class IMDb_Analyzer():
    """Analyzes TV series based on data from IMDb"""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.__driver.close()

    def execute_in_series_homepage(func):
        # try:
        #     series_header = self.__driver.find_element_by_css_selector(
        #         consts.SERIES_HEADER_CSL
        #     )
        #     assert series_name in series_header.text
        # except NoSuchElementException:
        #     print("Series title not found")
        def wrapper(*args, **kwargs):
            print(args)
            func(*args, **kwargs)
        return wrapper

    def query(self, series_name: str) -> None:
        """Query a TV series's ratings with its name.
        Return: a SeriesRating object
        """
        self._navigate_to_series(series_name)
        overall_rating = self._get_overall_rating(series_name)
        seasons_count = self._get_seasons_count(series_name)
        series_ratings = SeriesRatings(overall_rating=overall_rating,
                                       seasons_count=seasons_count)
        print(series_ratings)

    # @execute_in_series_homepage
    def _get_seasons_count(self, series_name: str) -> int:
        seasons_count_raw = self.__driver.find_element_by_css_selector(
            consts.SEASONS_COUNT_CSL
        )
        seasons_count = int(seasons_count_raw.text)
        return seasons_count

    def _get_overall_rating(self, series_name: str) -> float:
        overall_rating_raw = self.__driver.find_element_by_css_selector(
            consts.OVERALL_RATINGS_CSL
        )
        overall_rating = float(overall_rating_raw.text)
        return overall_rating

    def _navigate_to_series(self, name: str):
        self.__driver.get(consts.HOMEPAGE_URL)
        serach_bar = self.__driver.find_element_by_css_selector(
            consts.SEARCH_BAR_CSL
        )
        serach_bar.clear()
        serach_bar.send_keys(name)
        serach_bar.send_keys(Keys.ENTER)
        assert "Find - IMDb" in self.__driver.title
        first_result_box = self.__driver.find_element_by_css_selector(
            consts.SEARCH_RESULT_FIRST_FULL_BOX_CSL
        )
        assert consts.TV_SERIES_IDENTIFIER in first_result_box.text
        first_result = self.__driver.find_element_by_css_selector(
            consts.SEARCH_RESULT_FIRST_URL_CSL
        )
        assert name in first_result.text
        first_result.click()
