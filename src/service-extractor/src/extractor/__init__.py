import functools
import json
import logging
import os
from pathlib import Path
import pickle
from pprint import pprint
import requests
import time
from collections import OrderedDict
from datetime import datetime
from typing import List

from dotenv import load_dotenv

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from extractor.config import ExtractorConfig
from extractor.constants import IMDb_Constants as consts
from extractor.ratings import SeriesRatings, SeriesRatingsCollection

logger = logging.getLogger(__name__)


env_path = Path('.') / 'dev.env'
load_dotenv(dotenv_path=env_path)
DB_API = os.getenv("DB_API")


class RemoteDriver():
    def __init__(self):
        pass

    def __enter__(self):
        self.__driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        return self.__driver

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            print(exception_type, exception_value, traceback)
        self.__driver.quit()


class IMDb_Extractor():
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
                    series_header = self._IMDb_Extractor__driver\
                        .find_element_by_css_selector(
                            consts.SERIES_HEADER_CSL
                        )
                    if len(args) >= 1:
                        assert args[0] in series_header.text
                    else:
                        raise NoSeriesNameAsFirstArgException
                except NoSuchElementException:
                    logger.error("Series title not found")
                    quit()
                return func(self, *args, **kwargs)
            return wrapper

        def execute_in_series_episode_guide(func):
            """Decorator that enforces the wrapped function to be executed
            when the driver is on the Episode Guide page.
            """

            def wrapper(self, *args, **kwargs):
                assert (consts.EPISODES_GUIDE_IDENTIFIER
                        in self._IMDb_Extractor__driver.current_url), \
                    "Driver is not currently on the Episodes Guide page"
                return func(self, *args, **kwargs)
            return wrapper

        def wait_to_execute_in_series_season_page(func):
            """Decorator that enforces the wrapped function to be executed
            when the driver is on one of the season pages of a TV Series.
            """

            def wrapper(self, *args, **kwargs):
                # @timeout(delay=self._IMDb_Extractor__DELAY_SECS)
                def is_on_season_page():
                    url = self._IMDb_Extractor__driver.current_url
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
                    logger.error("No such element.")
                    quit()
            return wrapper

    def __init__(self, config: ExtractorConfig):
        chrome_options = Options()
        if config.headless:
            chrome_options.add_argument("--headless")
        self.__driver = None
        self.__PAGE_LOAD_TIMEOUT = 30
        self.__PAGE_LOAD_TIMEOUT_RETRY = 3

        self.__DELAY_SECS = 10

    def multiple_queries(self, series_names: List[str],
                         ratings_collection: SeriesRatingsCollection) -> None:
        """Query _multiple_ TV series' ratings with a List of their names.
        This is a convenient API that is equivalent to multiple `query` calls.
        """
        with RemoteDriver() as dvr:
            self.__driver = dvr
            for tv_series in series_names:
                if tv_series not in ratings_collection:
                    ratings = self.query(tv_series)
                    ratings_collection.add(ratings)
            else:
                logger.info("Data already exists; Noting to query in {}".format(
                    str(series_names)))

    def query(self, series_name: str) -> SeriesRatings:
        """Query a TV series's ratings with its name.
        Return: a SeriesRating object
        """
        print("Querying {}".format(series_name))
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
            season_num = index + 1
            season_ratings = self._query_ratings_in_season(season_num)
            if season_ratings is not None:
                series_ratings.add_season_ratings(season_num, season_ratings)

    @_Decorators.wait_to_execute_in_series_season_page
    def _query_ratings_in_season(self, season_num: int) -> List[float]:
        ratings = []
        try:
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
        except TimeoutException:
            logger.warning("Timeout in getting ratings for season {}. ".format(
                season_num),
                "This usually indicates this season has not aired yet.")
        return ratings if ratings != [] else None

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
        self._load_url(consts.HOMEPAGE_URL)
        search_bar = self.__driver.find_element_by_css_selector(
            consts.SEARCH_BAR_CSL
        )
        search_bar.clear()
        search_bar.send_keys(name)
        search_bar.send_keys(Keys.ENTER)
        first_result_box = self.__driver.find_element_by_css_selector(
            consts.SEARCH_RESULT_FIRST_FULL_BOX_CSL
        )
        assert any(
            ID in first_result_box.text for ID in consts.TV_SERIES_IDENTIFIERS)
        first_result = self.__driver.find_element_by_xpath(
            consts.SEARCH_RESULT_FIRST_URL_XPATH
        )
        assert name in first_result.text
        first_result.click()

    def _load_url(self, url: str):
        count = 1
        while count <= self.__PAGE_LOAD_TIMEOUT_RETRY:
            try:
                self.__driver.get(url)
            except TimeoutException:
                logger.error(
                    "Timeout loading {}, retrying attempt {}...".format(
                        url, count))
                continue
            finally:
                count += 1


def serialize(cls):
    class WrapperClass(cls):
        def __init__(self, *args, **kwargs):
            super(WrapperClass, self).__init__(*args, **kwargs)
            if self._IMDb_Queries_Manager__should_serialize \
                    and os.path.isfile(self._IMDb_Queries_Manager__pickle_name):
                with open(self._IMDb_Queries_Manager__pickle_name, 'rb') as pkl:
                    self._IMDb_Queries_Manager__ratings = pickle.load(pkl)
                    print("Deserialized!")

        def __del__(self):
            if self._IMDb_Queries_Manager__should_serialize:
                with open(self._IMDb_Queries_Manager__pickle_name, 'w+b') as pkl:
                    pickle.dump(self._IMDb_Queries_Manager__ratings, pkl)
                    print("Serialized!")
    return WrapperClass


# @serialize
class IMDb_Queries_Manager():
    """Fundamentally, an operational cycle involves 2 essential operations:
    querying, and data persistence. The queries manager composes the classes
    for these 2 operations together (IMDb_Extractor for querying, 
    SeriesRatingsCollection for data persistence).

    Composing these 2 operations allow us to make queries exactly _once_, 
    thereby avoiding multiple deserialization-serialization processes, which
    are very costly. 

    Users of the API are therefore advised to utilize this class, rather than
    the IMDb_Extractor and SeriesRatingsCollection classes.
    """

    class _Decorators():
        def serialize_ratings_if_configured(func):
            """Perform deserialization setup and serialization teardown for 
            methods modifying the ratings collection, if the serialization 
            option has been configured to be on. 
            """

    def __init__(self, config: ExtractorConfig):
        self.__config = config
        self.__should_serialize = config.should_serialize
        self.__pickle_name = config.serialization_filename
        self.__analyzer = None
        self.__ratings = SeriesRatingsCollection()
        self.__queries = set()

    def add_query(self, query: str) -> None:
        """Queue up queries to be executed. Queries are added onto the waiting 
        list, but _not executed_. Please call the `execute()` for execution.
        Add_query is indempotent; repeatedly adding the same query will not
        raise a warning or error.
        """
        self.__queries.add(query)

    def add_multiple_queries(self, queries: List[str]) -> None:
        """Queue up multiple queries to be executed. Queries are added onto 
        the waiting list, but _not executed_. Please call the `execute()` 
        for execution.

        Adding multiple queries is indempotent; if a certain query alreaady
        exists in the pending list, it would not be added twice.
        """
        self.__queries = self.__queries.union(set(queries))

    @property
    def pending_queries(self) -> List[str]:
        return list(self.__queries)

    def _clear_pending_queries(self) -> None:
        self.__queries.clear()

    def local_execute(self) -> None:
        """Execute all pending queries."""
        self.__analyzer.multiple_queries(series_names=self.__queries.keys(),
                                         ratings_collection=self.__ratings)
        self._clear_pending_queries()

    def api_execute(self) -> None:
        queries = []

        for q in self.__queries:
            r = requests.get(url=DB_API, params={'name': q})
            if r.status_code != 200:
                queries.append(q)

        if len(queries) == 0:
            return True

        if self.__analyzer is None:
            self.__analyzer = IMDb_Extractor(self.__config)
        self.__analyzer.multiple_queries(queries, self.__ratings)

        jsons = list(map(lambda r: r.json, self.__ratings.collection.values()))
        pprint(jsons)

        success = True
        for json_obj in jsons:
            r = requests.post(url=DB_API, json=json_obj)
            print("POST STATUS: ", r.status_code)
            if r.status_code != 200:
                success = False

        self._clear_pending_queries()
        return success
