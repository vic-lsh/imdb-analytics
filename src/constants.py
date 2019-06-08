class IMDb_Constants():
    """Constants that are used to select IMDB page elements.
    """

    HOMEPAGE_URL = "https://www.imdb.com/"

    TV_SERIES_IDENTIFIER = "TV Series"

    SEARCH_BAR_CSL = "#navbar-query"
    SEARCH_RESULT_TABLE_XPATH = "/html/body/div[1]/div/div[2]/div/div[1]/div/div[2]/table"
    SEARCH_RESULT_FIRST_FULL_BOX_CSL = "div.findSection:nth-child(3) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)"
    SEARCH_RESULT_FIRST_URL_CSL = "div.findSection:nth-child(3) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)"
