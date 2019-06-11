from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import DateTimeField, EmbeddedDocumentListField, \
    FloatField, IntField, ListField, StringField
import datetime


class EpisodeRating(EmbeddedDocument):
    """Model for Episode Rating embedded in `SeasonRatings`

    Attributes include:
        `@episode_number` [pk]: episode number
        `@season_number`: season number
        `@rating`: a _float_ defining this episode's rating (min: 0, max: 10)
    """
    season_number = IntField(min_value=1)
    episode_number = IntField(min_value=1, primary_key=True)
    rating = FloatField(min_value=0, max_value=10)


class SeasonRatings(EmbeddedDocument):
    """Model for Season Ratings embedded in `TVSeries`.

    Attributes include:
        `@season_number` [pk]: season number
        `@episodes_count`: number of episodes in this season
        `@ratings`: a list of `EpisodeRating` defines ratings in this season
    """
    season_number = IntField(min_value=1, primary_key=True)
    episodes_count = IntField(min_value=1)
    ratings = EmbeddedDocumentListField(document_type=EpisodeRating)


class TVSeries(Document):
    """Model for TV Series.

    Attributes include:
        `@name` [pk]: the name of the TV series
        `@last_modified`: automatically updates modification time when updated
        `@season_count`: number of seasons
        `@ratings`: a list of `SeasonRatings` stores all episode ratings
    """
    name = StringField(max_length=120, required=True, primary_key=True)
    last_modified = DateTimeField(default=datetime.datetime.utcnow)
    seasons_count = IntField(min_value=1)
    ratings = EmbeddedDocumentListField(document_type=SeasonRatings)
