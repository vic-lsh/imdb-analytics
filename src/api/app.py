import mongoengine

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from db import Database

app = Flask(__name__)
api = Api(app)


class TVSeriesCollection(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        assert request.is_json, "Fmt error"
        return request.json


class TVSeries(Resource):
    def get(self, identifier: str):
        with Database() as db:
            resp = db.find(identifier)
        if resp is None:
            return {'message': 'TVSeries not found'}, 404
        else:
            return resp.to_json()

    def delete(Resource):
        return


api.add_resource(TVSeriesCollection, '/tv-series')
api.add_resource(TVSeries, '/tv-series/<string:identifier>')


if __name__ == '__main__':
    app.run(debug=True)
