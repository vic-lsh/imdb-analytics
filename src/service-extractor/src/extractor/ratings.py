import logging
from typing import List

logger = logging.getLogger(__name__)

SERIES_NAME_MAXLEN = 100


class SeriesRatings():
    """Data structure that contains rating-related info on a TV series"""

    def __init__(self, series_name: str,
                 overall_rating: float = None, seasons_count: int = None):
        """Initializes SeriesRatings.

        Params
        ------
        - `series_name`: str, required
        - `overall_rating`: float, optional, can be set via 
            `set_overall_rating`
        - `seasons_count`: int, optional, can be set via `set_seasons_count`.
            `season_count` cannot be modified once it has been set, whether
            set during initialization or via `set_seasons_count`.
        """
        self._validate_args(series_name, overall_rating, seasons_count)
        self.__SERIES_NAME = series_name
        self.__OVERALL_RATING = overall_rating
        self.__SEASONS_COUNT = seasons_count
        self.__episode_ratings = {}
        self.__max_episode_num = 0

    @property
    def series_name(self):
        """Returns the name of the series"""
        return self.__SERIES_NAME

    @property
    def seasons_count(self) -> int:
        """Returns the number of seasons this TV show has"""
        return self.__SEASONS_COUNT

    @property
    def overall_rating(self):
        """Returns the TV show's overall rating. 

        Each TV show has one unique overall rating only. The overall rating
        need not be the arithmetic mean of the show's episode ratings.
        """
        return self.__OVERALL_RATING

    @property
    def rating_values(self):
        """Returns episode ratings for the client to read and manipulate.

        `episode_ratings` is a dict of lists:
        {
            `season_number`: [
                ep_1_rating, ep_2_rating, ...    
            ]
        }
        """
        # TODO: it is probably a good idea to make `SeriesRatings` iterable,
        # rather than to directly return the dict of lists object.
        return self.__episode_ratings

    @property
    def json(self):
        return self._to_json()

    def set_overall_rating(self, rating: float) -> None:
        """Set the overall rating of a TV series."""
        if self.__OVERALL_RATING is not None:
            logger.warning("Overall rating is being modified.",
                           "Once set, overall rating should not be modified.")
        self.__OVERALL_RATING = rating

    def set_season_count(self, seasons_count: int) -> None:
        """Sets the number of seasons for the TV series. If season count has 
        been set (is not `None`), this method does _not_ override the existing
        season count with the value passed in. Once set, season count cannot
        and should not be modified.
        """
        if self.__SEASONS_COUNT is not None:
            logger.error("Season count is a constant ",
                         "and cannot be modified once it has been set.")
        else:
            self.__SEASONS_COUNT = seasons_count

    def add_season_ratings(self, season_num: int,
                           season_ratings: List[float]) -> None:
        """Add the ratings of a season to the TV series.

        Ratings in a season are defined by:
        - which season (season number)
        - episode ratings in that season
        """
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

    def _validate_args(self, series_name: str,
                       overall_rating: float = None, seasons_count: int = None):
        """Performs argument validation for SeriesRatings. Ensures that 
        arguments passed in are of the types listed in `__init__`'s signature.

        In addition, ensures that:

        - 0 < len(series_name) <= 100 (`series_name` cannot be an empty string)
        - 0 <= overall_rating <= 10 
        = seasons_count > 0

        Raises
        ------
        `SeriesNameTypeError`
            raised when `series_name` is not of string type

        `OverallRatingTypeError`
            raised when `overall_rating` is specified and not of float type

        `SeasonsCountTypeError`
            raised when `season_count` is specified and not of int type

        `SeriesNameValueError`
            raised when `series_name` is empty or too long

        `OverallRatingValueError`
            raised when `overall_rating` is not between 0-10

        `SeasonsCountValueError`
            raised when `seasons_count` is non-positive
        """

        # validate arg types
        if not isinstance(series_name, str):
            raise SeriesNameTypeError("Series name must be a string.")
        if overall_rating is not None and not isinstance(overall_rating, float):
            raise OverallRatingTypeError(
                ("Rating value (`overall_rating`) must be a float. "
                 "If your rating is a round number (e.g. `9`), "
                 "use `9.0` rather than `9`."))
        if seasons_count is not None and not isinstance(seasons_count, int):
            raise SeasonsCountTypeError("Seasons count must be an int.")

        # validate arg values
        if not series_name:
            raise SeriesNameValueError(
                "Series name must not be an empty string.")
        if len(series_name) > SERIES_NAME_MAXLEN:
            raise SeriesNameValueError(("Series name cannot be longer than "
                                        f"{SERIES_NAME_MAXLEN} characters."))
        if overall_rating is not None and not (0 <= overall_rating <= 10):
            raise OverallRatingValueError(
                "Overall rating must be a float between 0 and 10.")
        if seasons_count is not None and not (seasons_count > 0):
            raise SeasonsCountValueError(
                "Seasons count must be an positive integer.")

    def _to_json(self) -> dict:
        """The internal implementation of ratings serialization.

        Serializes to the `SeriesRatings` class to a agreed-upon format that is
        accepted by other services. For instance, the database service does
        not know about `SeriesRatings`'s implementation; it only accepts a
        JSON of this format.

        Format description
        ------------------
        (update this section when updating the method)
        ```
        {
            "name": [series_name], 
            "series_rating": [the show's overall rating], 
            "episode_ratings": [
                {
                    "season": 1,
                    "ratings": [
                        { "episode_number": 1, "rating": 8.8 }
                        { "episode_number": 2, "rating": 9.3 }
                    ]
                },
                ...
            ]
        }
        ```
        """
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

    def _validate_item_added(add_func):
        def add_func_wrapper(self, *args, **kwargs):
            if 'item' in kwargs:
                item = kwargs['item']
            elif 'item_to_add' in kwargs:
                item = kwargs['item_to_add']
            elif len(args) > 0:
                item = args[0]
            else:
                err_msg = ("Trying to perform validation for item to be "
                           "added, but no argument can be found in the "
                           "item-adding func.")
                raise AddValidatorUsageError(err_msg)
            try:
                assert isinstance(item, SeriesRatings)
            except:
                raise CollectionItemTypeError()
            return add_func(self, *args, **kwargs)
        return add_func_wrapper

    @_validate_item_added
    def add(self, item_to_add: SeriesRatings) -> None:
        """Add a `SeriesRatings` object to the `SeriesRatingsCollection`.

        Logs a warning if the TV series being added is already in the 
        collection.
        """
        name = item_to_add.series_name
        if name in self.__ratings_collection:
            logger.warning(("Ratings for show {} exists but is being modified. "
                            "This is usually unintentional and indicates "
                            "a bug.").format(name))
        self.__ratings_collection[name] = item_to_add

    def add_multiple(self, ratings_list: List[SeriesRatings]) -> None:
        """Add multiple SeriesRatings to the collection."""
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


class AddValidatorUsageError(Exception):
    """Raised when the internal decorator `_validate_item_added` is not used 
    as intended, for instance when the decorator is used on a function with
    no arguments (thus no `item_to_add` to validate)
    """
    pass


class CollectionItemTypeError(TypeError):
    """Raised when the item being added to SeriesRatingCollection is not a
    SeriesRatings object
    """
    pass


class SeriesNameTypeError(TypeError):
    """TypeError raised when SeriesName is not a string"""
    DEFAULT_MSG = "Series name must not be an empty string."

    def __init__(self, message=DEFAULT_MSG):
        super().__init__(message)


class OverallRatingTypeError(TypeError):
    """TypeError raised when OverallRating is not a float"""
    pass


class SeasonsCountTypeError(TypeError):
    """TypeError raised when seasons count is not a int"""
    pass


class SeriesNameValueError(ValueError):
    """ValueError for series name"""
    pass


class OverallRatingValueError(ValueError):
    """ValueError for overall rating"""
    pass


class SeasonsCountValueError(ValueError):
    """ValueError for seasons count"""
    pass
