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


def test_rating_set_season_count():
    """Tests that `season_count`, once set, cannot be modified"""

    s_init_w_scount = SeriesRatings(series_name="GOT", seasons_count=8)
    s_init_w_scount.set_season_count(10)
    assert s_init_w_scount.seasons_count == 8

    s_init_wo_scount = SeriesRatings(series_name="GOT")
    s_init_wo_scount.set_season_count(3)
    assert s_init_wo_scount.seasons_count == 3
    s_init_wo_scount.set_season_count(6)
    assert s_init_wo_scount.seasons_count == 3


def test_ratings_collection_contains():
    """Tests that for SeriesRatingsCollection objects, the syntax 
    `{xx} in {collection}` works
    """
    c = SeriesRatingsCollection()
    assert callable(getattr(c, '__contains__'))

    s1 = SeriesRatings(series_name="GOT")
    c.add(s1)
    assert s1.series_name in c


def test_ratings_collection_add_item():
    c = SeriesRatingsCollection()
    with pytest.raises(ratings.CollectionItemTypeError):
        c.add("Test")

    # test `add`
    s1 = SeriesRatings(series_name="GOT")
    c.add(s1)
    assert s1.series_name in c

    # test `add_multiple`
    series_name_list = ["GOT", "Chernobyl", "Friends", "Breaking Bad"]
    items_to_add = [SeriesRatings(series_name=sn) for sn in series_name_list]
    c.add_multiple(items_to_add)
    for name in series_name_list:
        assert name in c

    c.add_multiple([])

    with pytest.raises(ratings.CollectionItemTypeError):
        c.add_multiple("Test")
    with pytest.raises(ratings.CollectionItemTypeError):
        c.add_multiple(13)
