import traceback

import mongoengine

import db.models as models
from imdb.ratings import SeriesRatingsCollection


class IMDb_Database():

    def __init__(self):
        pass

    def __enter__(self):
        self.__db = mongoengine.connect(db='IMDb')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            traceback.print_exception(
                exception_type, exception_value, traceback)
        self.__db.close()

    @property
    def db(self):
        return self.__db

    @staticmethod
    def if_tv_series_exists(series_name: str) -> bool:
        return models.TVSeries.objects(name=series_name).count() > 0

    def add_multiple_ratings(self, ratings: SeriesRatingsCollection) -> None:
        print(ratings)
