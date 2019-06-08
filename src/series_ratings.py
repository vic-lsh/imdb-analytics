class SeriesRatings():
    """Data structure that contains rating-related info on a TV series"""

    def __init__(self, overall_rating: float = None, seasons_count: int = None):
        self.__overall_rating = overall_rating
        self.__SEASONS_COUNT = seasons_count
        self.__episode_ratings = []

    def add_overall_rating(self, rating: float) -> None:
        """Add overall rating of a TV series"""
        if self.__overall_rating != None:
            print("Warning: overall rating is being modified.",
                  "Once set, overall rating should not be modified.")
        self.__overall_rating = rating

    def set_season_count(self, seasons_count: int) -> None:
        """Set the number of seasons for a TV series.
        The method rejects modifications of season count, once it has been set.
        """
        if self.__SEASONS_COUNT != None:
            print("Error: season count is a constant ",
                  "and cannot be modified once it has been set.")
        else:
            self.__SEASONS_COUNT = seasons_count

    def __repr__(self):
        reprs = []
        reprs.append("Overall rating: \t{}".format(self.__overall_rating))
        reprs.append("Seasons count: \t{}".format(self.__SEASONS_COUNT))
        return "\n".join(reprs)
