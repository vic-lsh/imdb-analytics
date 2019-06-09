from typing import List


class SeriesRatings():
    """Data structure that contains rating-related info on a TV series"""

    def __init__(self, overall_rating: float = None, seasons_count: int = None):
        self.__overall_rating = overall_rating
        self.__SEASONS_COUNT = seasons_count
        self.__episode_ratings = {}
        self.__max_episode_num = 0

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

    def add_season_ratings(self, season_num: int, season_ratings: List[float]) -> None:
        if season_num in self.__episode_ratings and \
                self.__episode_ratings[season_num] != None:
            print("Warning: ratings for season {} has been set.".format(season_num),
                  "Modification of season warnings usually indicates a bug.")
        self.__episode_ratings[season_num] = season_ratings
        if len(season_ratings) > self.__max_episode_num:
            self.__max_episode_num = len(season_ratings)

    def __repr__(self):
        reprs = []
        reprs.append("Overall rating: \t{}".format(self.__overall_rating))
        reprs.append("Seasons count: \t{}".format(self.__SEASONS_COUNT))
        reprs.append(" \t" + "   ".join(["E{}".format(ep_num)
                                        for ep_num in range(self.__max_episode_num)]))
        for season_num, ratings in self.__episode_ratings.items():
            reprs.append("S{}\t".format(season_num) + "  ".join(map(str, ratings)))
        return "\n".join(reprs)
