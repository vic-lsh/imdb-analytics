"""
The API endpoints through which other services may request the crawler.
"""

from collections import deque
from datetime import datetime
import requests
import time
import threading

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
CORS(app)

jobs = {}
job_names = {}
job_queue = deque()
ctr = 1


def process_job_queue(timeout_secs: int = 10):
    print("sleeping {} secs".format(timeout_secs))
    time.sleep(timeout_secs)


class Job():
    __counter = 0
    __READY = 0
    __PROCESSING = 1
    __COMPLETED = 2

    def __init__(self, name: str):
        self.__jid = Job.__counter
        Job.__counter += 1
        self.__name = name
        self.__status = Job.__READY

    @property
    def id(self):
        return self.__jid

    @property
    def status(self):
        if self.__status == Job.__READY:
            return "Ready"
        elif self.__status == Job.__PROCESSING:
            return "Processing"
        elif self.__status == Job.__COMPLETED:
            return "Completed"

    def complete(self):
        self.__status = Job.__COMPLETED


class TVSeriesCrawlingJob(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('id', type=str)
        self._parser.add_argument('name', type=str)

    def get(self):
        args = self._parser.parse_args()
        id = args['id']
        if id not in jobs:
            return {'Message': 'The job you requested could not be found.'}, 404
        else:
            return jsonify(jobs[id])

    def post(self):
        args = self._parser.parse_args()
        name = args['name']

        if name in job_names:
            id = job_names[name]
            return {
                'Message': 'Job {} found. Status: {}'.format(id, jobs[id].status)
            }, 200
        else:
            job = Job(name)
            job_names[name] = job.id
            jobs[job.id] = job

            r = requests.get(url='http://localhost:8001/tv-series')
            if r.status_code == 200:
                job.complete()
            else:
                job_queue.append(job)
                return {'Message': 'Job {} accepted'.format(job.id)}, 202


api.add_resource(TVSeriesCrawlingJob, '/')


def flask_app():
    app.run(debug=True, port='0.0.0.0')


if __name__ == '__main__':
    t_main = threading.Thread(target=flask_app)
    t_process = threading.Thread(target=process_job_queue)

    t_main.start()
    t_process.start()
