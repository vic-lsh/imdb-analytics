import unittest
import requests

from tests.context import extractor, gateway

from gateway import app
from extractor.config import ExtractorConfig
from extractor import IMDb_Extractor


class TestGateway(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        self.cfg = ExtractorConfig()
        self.app = app
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        self.extr = IMDb_Extractor()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_main_route(self):
        resp = self.app.get('/', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
