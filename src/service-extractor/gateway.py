"""
The API endpoints through which other services may request the crawler.
"""

from flask import Flask
from flask_restful import Resource, reqparse, Api

from extractor.config import AnalyzerConfig
from extractor.extractor import IMDb_Queries_Manager


app = Flask(__name__)
api = Api(app)


class ExtractionJob(Resource):
    def __init__(self):
        self.psr = reqparse.RequestParser()
        self.psr.add_argument('name', type=str, required=True,
                              help="Required argument: the name of the TV show"
                              + " you want to scrape.")
        extractor_cfg = AnalyzerConfig()
        self.mgr = IMDb_Queries_Manager(extractor_cfg)

    def get(self):
        args = self.psr.parse_args()
        self.mgr.add_query(args['name'])
        successful = self.mgr.api_execute()
        if not successful:
            return {
                'Message': 'An error occured during execurint '
                + 'Job `{}`'.format(args['name'])
            }, 500
        return {
            'Message': 'Job `{}` executed successfully. '.format(args['name'])
        }, 200


api.add_resource(ExtractionJob, '/')

if __name__ == '__main__':
    app.run(debug=True)
