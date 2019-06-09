class IMDb_Constants():
    """Constants that are used to select IMDB page elements.

    Each constant is suffixed by the identifier type, useful in informing which 
    selenium driver API to call. Possible identifier types are as follows:
        URL:    url
        CSL:    CSS selector
        CSP:    CSS path
        XPATH:  xpath
    """

    HOMEPAGE_URL = "https://www.imdb.com/"

    TV_SERIES_IDENTIFIER = "TV Series"

    # IMDb homepage
    SEARCH_BAR_CSL = "#navbar-query"
    SEARCH_RESULT_TABLE_XPATH = "/html/body/div[1]/div/div[2]/div/div[1]/div/div[2]/table"
    SEARCH_RESULT_FIRST_FULL_BOX_CSL = "div.findSection:nth-child(3) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)"
    SEARCH_RESULT_FIRST_URL_CSL = "div.findSection:nth-child(3) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)"

    # TV Series homepage
    SERIES_HEADER_CSL = ".title_wrapper > h1:nth-child(1)"
    OVERALL_RATINGS_CSL = ".ratingValue > strong:nth-child(1) > span:nth-child(1)"
    SEASONS_COUNT_CSL = ".seasons-and-year-nav > div:nth-child(4) > a:nth-child(1)"
    EPISODE_GUIDE_DIV_CSL = ".bp_content"

    # TV Series episode guide page
    SEASONS_DROPDOWN_CSL = "#bySeason"
    SEASONS_DROPDOWN_ID = "bySeason"
    EPISODES_GUIDE_IDENTIFIER = "episodes?ref_=tt_ov_epl"
