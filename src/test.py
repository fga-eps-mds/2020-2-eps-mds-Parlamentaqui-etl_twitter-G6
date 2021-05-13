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

    # @requests_mock.Mocker()
    # def test_perfis_deputados_verificados_100(self, request_mock):
    #     url = (f"https://api.twitter.com/2/users/by?{usernames}&user.fields=verified,url")
    #     data = { }

    #     request_mock.get(url, json=data)
    #     request = self.client.get(url_for('api.perfis_deputados_verificados_100'))
    #     self.assertEqual(200 , request.status_code)

    # @requests_mock.Mocker()
    # def test_update_twitter_accounts(self, request_mock):
    #     url = (f"https://api.twitter.com/2/users/by?usernames={usernames_to_found}&user.fields=verified,url")
    #     data = { }
    #     data_expected = 'Done. Use url api/get_all_deputies for get all the deputies in db'

    #     request_mock.get(url, json=data)
    #     request = self.client.get(url_for('api.update_twitter_accounts'))
    #     self.assertEqual(200 , request.status_code)
    #     self.assertEqual(data_expected , request.data.decode())

    def test_api_update_tweets(self):
        data_expected = 'Updated tweets sucessfully. Now use /get_all_tweets to see the tweets'

        request = self.client.get(url_for('api.update_tweets'))
        self.assertEqual(data_expected , request.data.decode())

    def test_get_all_deputies_status(self):
        request = self.client.get(url_for('api.get_all_deputies'))
        self.assertEqual(200 , request.status_code)

    def test_get_all_tweets_status(self):
        request = self.client.get(url_for('api.get_all_tweets'))
        self.assertEqual(200 , request.status_code)

    def test_api_delete_all_tweets_propositions(self):
        data_expected = 'All propositions tweets were deleted'

        request = self.client.get(url_for('api.delete_all_tweets_propositions'))
        self.assertEqual(data_expected , request.data.decode())

    def test_api_get_all_tweets_propositions(self):
        data_not_expected = []

        request = self.client.get(url_for('api.get_all_tweets_propositions'))
        self.assertNotEqual(data_not_expected , request.data.decode())

    def test_api_update_tweets_propositions(self):
        data_expected = 'Done'

        request = self.client.get(url_for('api.update_tweets_propositions'))
        self.assertNotEqual(data_expected , request.data.decode())

    def test_get_all_propositions_status(self):
        request = self.client.get(url_for('api.get_all_propositions'))
        self.assertEqual(200 , request.status_code)

    def test_delete_all_tweets_status(self):
        data_expected = 'All tweets were deleted'

        request = self.client.get(url_for('api.delete_all_tweets'))
        self.assertNotEqual(data_expected , request.data.decode())
    

    def tearDown(self):
        self.context.pop()

if __name__=='__main__':
    unittest.main()
