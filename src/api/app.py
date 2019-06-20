import mongoengine

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from db import Database

app = Flask(__name__)
api = Api(app)


class TVSeries(Resource):
    def get(self, identifier: str):
        with Database() as db:
            resp = db.find(identifier)
        if resp is None:
            return {'message': 'TVSeries not found'}, 404
        else:
            return resp.to_json()

    def post(self):
        with Database() as db:
            resp, msgs = db.add_from_dict(request.json)
        if resp == False:
            return {'Messages': msgs}, 400
        return request.json

    def delete(Resource):
        return


api.add_resource(TVSeries, '/tv-series')


if __name__ == '__main__':
    app.run(debug=True)
