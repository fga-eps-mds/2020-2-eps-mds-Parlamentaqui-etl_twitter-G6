import unittest
# from unittest import TestCase#, mock
from flask import url_for
from app import app
import requests_mock
import os

BEARER_TOKEN_TWITTER = os.getenv('BEARER_TOKEN')

# Token que autoriza a busca por dados na API do Twitter pelo protocolo OAuth 2.0 (somente infos publicas no Twitter)
auth_header = {"Authorization": "Bearer {}".format(BEARER_TOKEN_TWITTER)}

class EtlTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_index(self):
        request = self.client.get(url_for('/'))
        self.assertEqual(200 , request.status_code)

    def test_index_status(self):
        request = self.client.get(url_for('/'))
        self.assertEqual(200 , request.status_code)

    def tearDown(self):
        self.context.pop()

# if __name__=='__main__':
#     unittest.main()
