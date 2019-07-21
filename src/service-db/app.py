import json
import logging
import logging.config

import mongoengine
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse

import utils
import settings
from db import Database

try:
    logging.config.fileConfig(utils.get_logger_cfg_fpath())
except FileNotFoundError as e:
    print(e)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)
CORS(app)


class TVSeries(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('name', type=str, required=True)

    def get(self):
        args = self._parser.parse_args()
        identifier = args['name']
        logger.info(f"Initiating GET `{identifier}`")

        with Database() as db:
            resp = db.find(identifier)

        if resp is None:
            logger.error(f"`{identifier}` could not be found in the database.")
            # successful = self._schedule_extraction_job(identifier)
            return {'message': 'TVSeries not found'}, 404
        else:
            logger.info((f"{identifier} found in database; "
                         "Returning the series' data."))
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

    def _schedule_extraction_job(self, series_name: str, retry: int = 3) -> bool:
        """Extraction job scheduler

        Schedules an extraction job if the series cannot be found in the 
        database.
        """
        logger.info(("Attempting to schedule a extraction job "
                     f"for `{series_name}`"))
        while retry >= 0:
            r = requests.post(settings.JOB_SERVICE_API, params={
                'name': series_name
            })
            if r.status_code == 202:
                logger.info(f'Job scheduling for {series_name} successful')
                return True
            else:
                retry -= 1
        logger.error((f'Job scheduling for {series_name} not successful, '
                      f'remaining tries: {retry}'))
        return False


api.add_resource(TVSeries, '/tv-series')


if __name__ == '__main__':
    app.run(debug=True, port='0.0.0.0')
