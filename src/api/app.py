import json
import mongoengine

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

from db import Database

app = Flask(__name__)
api = Api(app)


class TVSeries(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('name', type=str)

    def get(self):
        args = self._parser.parse_args()
        identifier = args['name']

        with Database() as db:
            resp = db.find(identifier)

        if resp is None:
            return {'message': 'TVSeries not found'}, 404
        else:
            return jsonify(json.loads(resp.to_json()))

    def post(self):
        with Database() as db:
            resp, msgs = db.add_from_dict(request.json)

        if resp == False:
            return {'Messages': msgs}, 400
        return request.json

    def delete(self):
        args = self._parser.parse_args()
        identifier = args['name']

        with Database() as db:
            status = db.delete(identifier)

        if status == False:
            return {'message': 'TVSeries not found'}, 404
        else:
            return {'message': 'Deleted'}, 204


api.add_resource(TVSeries, '/tv-series')


if __name__ == '__main__':
    app.run(debug=True)
