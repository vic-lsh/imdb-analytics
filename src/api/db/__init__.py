import traceback

import mongoengine

from db.models import TVSeries, SeasonRatings, EpisodeRating


class Database():

    def __init__(self):
        self.__DB_NAME = 'imdb'

    def __enter__(self):
        self.__db = mongoengine.connect(db=self.__DB_NAME, host='mongo')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            print(exception_type, exception_value, traceback)
        self.__db.close()

    def find(self, series_name: str) -> TVSeries:
        print("querying")
        if self.if_tv_series_exists(series_name):
            print("done")
            return TVSeries.objects.with_id(self._get_id(series_name))
        else:
            print("done")
            return None

    def delete(self, series_name: str):
        """Deletes a series with the `series_name` provided.
        Returns True if the object is deleted, False if not deleted.
        """
        if self.if_tv_series_exists(series_name):
            resp = TVSeries.objects.with_id(self._get_id(series_name)).delete()
            return True
        return False

    def if_tv_series_exists(self, series_name: str) -> bool:
        return TVSeries.objects(name=series_name).count() > 0

    def add_from_dict(self, req: dict) -> bool:
        err = []

        MISSING_KEY_MSG = 'Some of the following keys are missing in {}: {}'

        required_root_level_keys = ('name', 'series_rating', 'episode_ratings')
        required_season_level_keys = ('season', 'ratings')
        required_episode_keys = ('episode_number', 'rating')
        
        tv_identifier = self._get_id(req['name'])

        try:
            tv_doc = TVSeries(identifier=tv_identifier, name=req['name'],
                              seasons_count=len(req['episode_ratings']),
                              overall_rating=req['series_rating'])
        except KeyError:
            err.append(MISSING_KEY_MSG.format(
                'root', required_root_level_keys))
            return False, err

        try:
            for season in req['episode_ratings']:
                season_doc = SeasonRatings(
                    season_number=season['season'],
                    episodes_count=len(season['ratings']))

                try:
                    for episode in season['ratings']:
                        season_doc.ratings.append(
                            EpisodeRating(
                                episode_number=episode['episode_number'],
                                rating=episode['rating'])
                        )
                except KeyError:
                    err.append(MISSING_KEY_MSG.format(
                        'episode_ratings', required_episode_keys))
                    return False, err

                tv_doc.ratings.append(season_doc)

            tv_doc.save()
        except KeyError:
            err.append(MISSING_KEY_MSG.format(
                'season', required_season_level_keys))
            return False, err

        return len(err) == 0, err

    def _get_id(self, name: str): 
        def process_char(c: str):
            if c.isalnum():
                return c.lower()
            elif c == ' ':
                return '_'
            else:
                return ''
        return ''.join(process_char(c) for c in name)