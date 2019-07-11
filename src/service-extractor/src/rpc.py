import logging
import time
from concurrent import futures

import grpc

from extractor import IMDb_Queries_Manager
from extractor.config import ExtractorConfig
from proto import imdb_pb2, imdb_pb2_grpc

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class ExtractionService(imdb_pb2_grpc.ExtractorServiceServicer):
    def __init__(self, *args, **kwargs):
        self.mgr = IMDb_Queries_Manager(ExtractorConfig())

    def InitiateExtraction(self, request, context):
        # TODO: implement `is_item_name_valid`
        # currently this attribute defaults to True
        logger.info("Requesting to extract `{}`".format(request.item_name))
        self.mgr.add_query(request.item_name)
        successful = self.mgr.api_execute()
        logger.info("Request `{}` finished; success status: {}"
                    .format(request.item_name, successful))
        return imdb_pb2.ExtractionResponse(
            is_item_name_valid=True, successful=successful)


def serve():
    PORT = ":8989"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imdb_pb2_grpc.add_ExtractorServiceServicer_to_server(
        ExtractionService(), server)
    server.add_insecure_port('[::]{}'.format(PORT))
    server.start()
    logger.info("Server started at port{}".format(PORT))
    try:
        while True:
            time.sleep(60 * 60 * 12)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
