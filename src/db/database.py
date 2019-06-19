import traceback

import mongoengine

from db.models import TVSeries, SeasonRatings, EpisodeRating
from imdb.ratings import SeriesRatingsCollection


class IMDb_Database():

    def __init__(self):
        pass

    def __enter__(self):
        self.__db = mongoengine.connect(db='imdb')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            traceback.print_exception(
                exception_type, exception_value, traceback)
        self.__db.close()

    @property
    def db(self):
        return self.__db

    def if_tv_series_exists(self, series_name: str) -> bool:
        return TVSeries.objects(name=series_name).count() > 0

    def delete(self, series_name: str):
        if self.if_tv_series_exists(series_name):
            TVSeries.objects.with_id(series_name).delete()

    def find(self, series_name: str) -> TVSeries:
        if self.if_tv_series_exists(series_name):
            return TVSeries.objects.with_id(series_name)

    def add_multiple_ratings(
            self, ratings_collection: SeriesRatingsCollection) -> None:
        for series_name, ratings in ratings_collection.collection.items():
            series_doc = TVSeries(name=series_name,
                                  seasons_count=ratings.seasons_count,
                                  overall_rating=ratings.overall_rating)

            for season_num, season_ratings in ratings.rating_values.items():
                season_rating_doc = SeasonRatings(season_number=season_num,
                                                  episodes_count=len(season_ratings))
                episode_ctr = 1
                for episode_rating in season_ratings:
                    season_rating_doc.ratings.append(
                        EpisodeRating(season_number=season_num,
                                      episode_number=episode_ctr,
                                      rating=episode_rating)
                    )
                    episode_ctr += 1
                series_doc.ratings.append(season_rating_doc)

            series_doc.save()
