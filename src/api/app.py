import mongoengine

from flask import Flask, g
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


def get_db():
    """Maintains a single database connection throughout the app lifetime.
    Creates a new db connection if one does not already exist.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mongoengine.connect(db='imdb')
    return db


class TVSeriesCollection(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return


class TVSeries(Resource):
    def get(self):
        return

    def delete(Resource):
        return

api.add_resource(TVSeriesCollection, '/tv-series')

if __name__ == '__main__':
    app.run(debug=True)
