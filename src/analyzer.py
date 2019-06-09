from datetime import datetime
import functools
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from constants import IMDb_Constants as consts
from series_ratings import SeriesRatings


class IMDb_Analyzer():
    """Analyzes TV series based on data from IMDb"""

    class ElementStalessTimeoutException:
        """Exception raised when element remains stale (accessing it raises 
        StaleElementReferenceException) for `timeout` seconds.
        """
        pass

    class _Decorators():
        def execute_in_series_homepage(func):
            """Decorator that enforces the wrapped function to be run only if 
            the driver is on the TV series' home page.

            Raises: 
                NoSuchElementException:
                    if the driver is not on the series' home page.
                NoSeriesNameAsFirstArgException:
                    if the wrapped function does not provide `series_name` as
                    its first argument, without which the decorator cannot check.
            """

            def wrapper(self, *args, **kwargs):
                class NoSeriesNameAsFirstArgException(Exception):
                    """To use the `catch_no_such_element_exception` decorator, 
                    the wrapped function must provide `series_name` as its 
                    first argument.
                    """

                    def __init__(self, message=None, payload=None):
                        self.message = "Please provide `series name`"\
                            + " as your first argument."
                        self.payload = payload

                    def __str__(self):
                        return str(self.message)
                try:
                    series_header = self._IMDb_Analyzer__driver\
                        .find_element_by_css_selector(
                            consts.SERIES_HEADER_CSL
                        )
                    if len(args) >= 1:
                        assert args[0] in series_header.text
                    else:
                        raise NoSeriesNameAsFirstArgException
                except NoSuchElementException:
                    print("Series title not found")
                    sys.exit(1)
                return func(self, *args, **kwargs)
            return wrapper

        def execute_in_series_episode_guide(func):
            """Decorator that enforces the wrapped function to be executed
            when the driver is on the Episode Guide page.
            """

            def wrapper(self, *args, **kwargs):
                assert (consts.EPISODES_GUIDE_IDENTIFIER
                        in self._IMDb_Analyzer__driver.current_url), \
                    "Driver is not currently on the Episodes Guide page"
                return func(self, *args, **kwargs)
            return wrapper

        def catch_no_such_element_exception(elem_accessing_func):
            def wrapper(*args, **kwargs):
                try:
                    return elem_accessing_func(*args, **kwargs)
                except NoSuchElementException:
                    print("No such element.")
                    sys.exit(1)
            return wrapper

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.__driver.close()

    def query(self, series_name: str) -> None:
        """Query a TV series's ratings with its name.
        Return: a SeriesRating object
        """
        self._navigate_to_series(series_name)
        overall_rating = self._get_overall_rating(series_name)
        seasons_count = self._get_seasons_count(series_name)
        series_ratings = SeriesRatings(overall_rating=overall_rating,
                                       seasons_count=seasons_count)
        self._navigate_to_episode_guide(series_name)
        self._query_episode_ratings()

    @_Decorators.catch_no_such_element_exception
    @_Decorators.execute_in_series_episode_guide
    def _query_episode_ratings(self) -> None:
        season_dropdown = Select(self.__driver.find_element_by_css_selector(
            consts.SEASONS_DROPDOWN_CSL
        ))
        seasons = season_dropdown.options
        for index in range(0, len(seasons) - 1):
            TIMEOUT_SECS = 10
            start_time = datetime.now()
            while True:
                try:
                    season_dropdown_elem = self.__driver.find_element_by_id(
                        consts.SEASONS_DROPDOWN_ID
                    )
                    season_dropdown = Select(season_dropdown_elem)
                    season_dropdown.select_by_index(index)
                    break
                except StaleElementReferenceException:
                    continue
                finally:
                    if (datetime.now() - start_time).seconds > TIMEOUT_SECS:
                        raise ElementStalessTimeoutException
                        break

    @_Decorators.catch_no_such_element_exception
    @_Decorators.execute_in_series_homepage
    def _navigate_to_episode_guide(self, series_name: str) -> None:
        self.__driver.find_element_by_css_selector(
            consts.EPISODE_GUIDE_DIV_CSL
        ).click()

    @_Decorators.catch_no_such_element_exception
    @_Decorators.execute_in_series_homepage
    def _get_seasons_count(self, series_name: str) -> int:
        seasons_count_raw = self.__driver.find_element_by_css_selector(
            consts.SEASONS_COUNT_CSL
        )
        seasons_count = int(seasons_count_raw.text)
        return seasons_count

    @_Decorators.catch_no_such_element_exception
    @_Decorators.execute_in_series_homepage
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
        # assert "Find - IMDb" in self.__driver.title
        first_result_box = self.__driver.find_element_by_css_selector(
            consts.SEARCH_RESULT_FIRST_FULL_BOX_CSL
        )
        assert consts.TV_SERIES_IDENTIFIER in first_result_box.text
        first_result = self.__driver.find_element_by_css_selector(
            consts.SEARCH_RESULT_FIRST_URL_CSL
        )
        assert name in first_result.text
        first_result.click()
