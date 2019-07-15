import pytest

from tests.context import extractor
from extractor.ratings import SeriesRatings, SeriesRatingsCollection
import extractor.ratings as ratings


def test_rating_properties():
    """Tests SeriesRatings's @property methods return the values set during 
    initialization.
    """
    series_name = "Game of Thrones"
    overall_rating = 9.3
    seasons_count = 8

    sr = SeriesRatings(series_name=series_name,
                       overall_rating=overall_rating,
                       seasons_count=seasons_count)

    assert sr.series_name == series_name
    assert sr.overall_rating == overall_rating
    assert sr.seasons_count == seasons_count


def test_rating_init_typechecks():
    """Tests SeriesRatings's ability to raise errors if the values used in
    initialization do not pass type validation.
    """

    # series name must be a string
    with pytest.raises(ratings.SeriesNameTypeError):
        s = SeriesRatings(series_name=33)

    # overall rating must be a float
    with pytest.raises(ratings.OverallRatingTypeError):
        s = SeriesRatings(series_name="GOT", overall_rating=9)

    # seasons count must be an int
    with pytest.raises(ratings.SeasonsCountTypeError):
        s = SeriesRatings(series_name="GOT",
                          overall_rating=9.0, seasons_count='a')

    # series name cannot be empty string
    with pytest.raises(ratings.SeriesNameValueError):
        s = SeriesRatings(series_name="")

    # series_name cannot be longer than 100 chars
    with pytest.raises(ratings.SeriesNameValueError):
        s = SeriesRatings(series_name=(
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        ))

    # no negative value for overall_rating
    with pytest.raises(ratings.OverallRatingValueError):
        s = SeriesRatings(series_name="GOT", overall_rating=-1.9)

    # overall rating must be < 10
    with pytest.raises(ratings.OverallRatingValueError):
        s = SeriesRatings(series_name="GOT", overall_rating=122.21)

    # season count must be > 0
    with pytest.raises(ratings.SeasonsCountValueError):
        s = SeriesRatings(series_name="GOT",
                          overall_rating=9.0, seasons_count=0)

    # season count must be > 0
    with pytest.raises(ratings.SeasonsCountValueError):
        s = SeriesRatings(series_name="GOT",
                          overall_rating=9.0, seasons_count=-5)