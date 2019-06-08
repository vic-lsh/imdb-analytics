from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from constants import IMDb_Constants as consts


class IMDb_Analyzer():
    """Analyzes TV series based on data from IMDb"""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.__driver.close()

    def query(self, name: str) -> None:
        """Query a TV series's ratings with its name"""
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
