import logging
from typing import List

logger = logging.getLogger(__name__)


class SeriesRatings():
    """Data structure that contains rating-related info on a TV series"""

    def __init__(self, series_name: str,
                 overall_rating: float = None, seasons_count: int = None):
        self.__SERIES_NAME = series_name
        self.__OVERALL_RATING = overall_rating
        self.__SEASONS_COUNT = seasons_count
        self.__episode_ratings = {}
        self.__max_episode_num = 0

    @property
    def series_name(self):
        return self.__SERIES_NAME

    @property
    def seasons_count(self):
        return self.__SEASONS_COUNT

    @property
    def overall_rating(self):
        return self.__OVERALL_RATING

    @property
    def rating_values(self):
        return self.__episode_ratings

    @property
    def json(self):
        return self._to_json()

    def add_overall_rating(self, rating: float) -> None:
        """Add overall rating of a TV series"""
        if self.__OVERALL_RATING is not None:
            logger.warning("Overall rating is being modified.",
                           "Once set, overall rating should not be modified.")
        self.__OVERALL_RATING = rating

    def set_season_count(self, seasons_count: int) -> None:
        """Set the number of seasons for a TV series.
        The method rejects modifications of season count, once it has been set.
        """
        if self.__SEASONS_COUNT is not None:
            logger.error("Season count is a constant ",
                         "and cannot be modified once it has been set.")
        else:
            self.__SEASONS_COUNT = seasons_count

    def add_season_ratings(self, season_num: int,
                           season_ratings: List[float]) -> None:
        if season_num in self.__episode_ratings and \
                self.__episode_ratings[season_num] is not None:
            logger.warning(("Ratings for season {} has been set. Modification "
                            "of season warnings usually indicates "
                            "a bug.").format(season_num))
        self.__episode_ratings[season_num] = season_ratings
        if len(season_ratings) > self.__max_episode_num:
            self.__max_episode_num = len(season_ratings)

    def __str__(self):
        reprs = []
        DESC_STR = ("Overall rating: {}\t".format(self.__OVERALL_RATING) +
                    "Seasons count:  {}".format(self.__SEASONS_COUNT))
        HEADER_STR = "      " + "".join(["E{:<4}".format(ep_num)
                                         for ep_num in range(
                                             self.__max_episode_num)])
        SPACE_LEN = 2
        banner_len = (max(len(HEADER_STR), len(DESC_STR)) -
                      len(self.__SERIES_NAME) - 2 * SPACE_LEN) // 2
        if banner_len < 2:
            banner_len = 2
        reprs.append("*" * banner_len + " " * SPACE_LEN +
                     self.__SERIES_NAME + " " * SPACE_LEN + "*" * banner_len)
        reprs.append(DESC_STR)
        reprs.append(HEADER_STR)
        for season_num, ratings in self.__episode_ratings.items():
            reprs.append("S{:<5}".format(season_num) +
                         "  ".join(map(str, ratings)))
        reprs.append("")
        return "\n".join(reprs)

    def __repr__(self):
        return self.__str__

    def _to_json(self):
        json_obj = {
            'name': self.__SERIES_NAME,
            'series_rating': self.__OVERALL_RATING,
            'episode_ratings': []
        }
        for season_num, season_ratings in self.__episode_ratings.items():
            obj = {}
            ep_ctr = 1
            obj['season'] = season_num
            obj['ratings'] = []
            for ep_rating in season_ratings:
                obj['ratings'].append({
                    'episode_number': ep_ctr,
                    'rating': ep_rating
                })
                ep_ctr += 1
            json_obj['episode_ratings'].append(obj)
        return json_obj


class SeriesRatingsCollection():
    """A collection of `SeriesRatings` objects"""

    def __init__(self):
        self.__ratings_collection = {}

    @property
    def collection(self):
        return self.__ratings_collection

    def add(self, ratings: SeriesRatings) -> None:
        name = ratings.series_name
        if name in self.__ratings_collection:
            logger.warning("Ratings for show {} exists but is being modified. "
                           + "This is usually unintentional and indicates "
                           + "a bug.".format(name))
        self.__ratings_collection[name] = ratings

    def add_multiple(self, ratings_list: List[SeriesRatings]) -> None:
        for ratings in ratings_list:
            self.add(ratings)

    def __contains__(self, item):
        assert isinstance(item, str)
        return item in self.__ratings_collection

    def __len__(self):
        return len(self.__ratings_collection)

    def __repr__(self):
        reprs = []
        for _, ratings in self.__ratings_collection.items():
            reprs.append(ratings.__str__())
        return "\n".join(reprs)
