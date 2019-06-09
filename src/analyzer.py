from datetime import datetime
import functools
import sys
import time
from typing import List

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
from ratings import SeriesRatings
from utils import timeout


class IMDb_Analyzer():
    """Analyzes TV series based on data from IMDb"""

    class ElementStalessTimeoutException(Exception):
        """Exception raised when element remains stale (accessing it raises 
        StaleElementReferenceException) for `timeout` seconds.
        """
        pass

    class URLRedirectionTimeoutException(Exception):
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

        def wait_to_execute_in_series_season_page(func):
            """Decorator that enforces the wrapped function to be executed
            when the driver is on one of the season pages of a TV Series.
            """

            def wrapper(self, *args, **kwargs):
                @timeout(delay=self._IMDb_Analyzer__DELAY_SECS)
                def is_on_season_page():
                    url = self._IMDb_Analyzer__driver.current_url
                    error_msg = "Driver is currently not on a Season page"
                    assert(
                        consts.EPISODE_GUIDE_SEASON_PAGE_IDENTIFIER in url
                    ), error_msg
                return func(self, *args, **kwargs)
            return wrapper

        def catch_no_such_element_exception(elem_accessing_func):
            def wrapper(self, *args, **kwargs):
                try:
                    return elem_accessing_func(self, *args, **kwargs)
                except NoSuchElementException:
                    print("No such element.")
                    sys.exit(1)
            return wrapper

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome(options=chrome_options)
        self.__DELAY_SECS = 10

    def __del__(self):
        self.__driver.close()

    def query(self, series_name: str) -> None:
        """Query a TV series's ratings with its name.
        Return: a SeriesRating object
        """
        self._navigate_to_series(series_name)
        overall_rating = self._get_overall_rating(series_name)
        seasons_count = self._get_seasons_count(series_name)
        rating_series = SeriesRatings(series_name=series_name,
                                      overall_rating=overall_rating,
                                      seasons_count=seasons_count)
        self._navigate_to_episode_guide(series_name)
        self._query_episode_ratings(rating_series)
        return rating_series

    @_Decorators.catch_no_such_element_exception
    @_Decorators.execute_in_series_episode_guide
    def _query_episode_ratings(self, series_ratings: SeriesRatings) -> None:
        season_dropdown = Select(self.__driver.find_element_by_css_selector(
            consts.SEASONS_DROPDOWN_CSL
        ))
        seasons = season_dropdown.options
        for index in range(0, len(seasons)):
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
            season_ratings = self._query_ratings_in_season()
            series_ratings.add_season_ratings((index + 1), season_ratings)

    @_Decorators.wait_to_execute_in_series_season_page
    def _query_ratings_in_season(self) -> List[float]:
        ratings = []
        rating_divs = WebDriverWait(self.__driver, self.__DELAY_SECS).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, consts.EPISODE_RATINGS_CSL)
            )
        )
        episodes_num = len(rating_divs)
        for rating in rating_divs:
            ratings.append(float(rating.text))
        assert episodes_num == len(ratings), \
            "# of episodes and # of ratings do not match"
        return ratings

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
        first_result_box = self.__driver.find_element_by_css_selector(
            consts.SEARCH_RESULT_FIRST_FULL_BOX_CSL
        )
        assert consts.TV_SERIES_IDENTIFIER in first_result_box.text
        first_result = self.__driver.find_element_by_css_selector(
            consts.SEARCH_RESULT_FIRST_URL_CSL
        )
        assert name in first_result.text
        first_result.click()
