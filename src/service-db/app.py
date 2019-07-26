import logging
import logging.config

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api

from common import utils
from db import Database
from resources.tvseries import TVSeries

try:
    logging.config.fileConfig(utils.get_logger_cfg_fpath())
except FileNotFoundError as e:
    print(e)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)
CORS(app)


api.add_resource(TVSeries, '/tv-series')


if __name__ == '__main__':
    app.run(debug=True, port='0.0.0.0')
