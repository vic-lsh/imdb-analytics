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
            return TVSeries.objects.with_id(series_name)
        else:
            print("done")
            return None

    def if_tv_series_exists(self, series_name: str) -> bool:
        return TVSeries.objects(name=series_name).count() > 0

    def add_from_dict(self, req: dict) -> bool:
        successful = True
        msgs = []

        required_first_level_keys = (
            'name', 'series_rating', 'episode_ratings')
        if not all(k in req for k in required_first_level_keys):
            successful = False
            msgs.append("First-level key error")
            return successful, msgs

        try:
            tv_doc = TVSeries(name=req['name'],
                              seasons_count=len(req['episode_ratings']),
                              overall_rating=req['series_rating'])

            try:
                for season in req['episode_ratings']:
                    assert type(season) == dict

                    # season_required_keys = ('season', 'ratings')
                    # missing_keys = filter(lambda k: not(k in season), season_required_keys)
                    # if len(missing_keys) > 0:
                    #     msgs.append("Missing key(s) {}".format(str(missing_keys)))

                    season_doc = SeasonRatings(season_number=season['season'],
                                               episodes_count=len(season['ratings']))

                    try:
                        for episode in season['ratings']:
                            assert type(episode) == dict

                            ep = EpisodeRating(episode_number=episode['episode_number'],
                                               rating=episode['rating'])
                            season_doc.ratings.append(ep)

                        tv_doc.ratings.append(season_doc)
                    except:
                        successful = False
                        msgs.append("Episode parsing error")

                tv_doc.save()
            except:
                successful = False
                msgs.append("Season parsing error")

        except:
            successful = False
            msgs.append("TV Series creation error")

        return successful, msgs
