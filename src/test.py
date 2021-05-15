import unittest
from app import app
from mongoengine import connect
from flask import Flask
import requests_mock
import os

# Token que autoriza a busca por dados na API do Twitter pelo protocolo OAuth 2.0 (somente infos publicas no Twitter)
auth_header = {"Authorization": "Bearer {}".format(BEARER_TOKEN_TWITTER)}

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
PORT = os.getenv('PORT')

class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_index_status(self):
        request = self.client.get('/')
        self.assertEqual(200 , request.status_code)

    def test_index(self):
        request = self.client.get('/')
        self.assertEqual('ETL Twitter' , request.data.decode())
        self.assertGreaterEqual(len(request.data.decode()),2)

    def test_fake_status(self):
        request = self.client.get('/not_exist')
        self.assertEqual(404 , request.status_code)

    def tearDown(self):
        self.context.pop()


class EtlApiTests(unittest.TestCase):

    connect(DB_NAME, host=f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin')

    # @requests_mock.Mocker()
    # def test_perfis_deputados_verificados_100(self, request_mock):
    #     url = (f"https://api.twitter.com/2/users/by?{usernames}&user.fields=verified,url")
    #     data = { }

    #     request_mock.get(url, json=data)
    #     request = self.client.get('/api/perfis_deputados_verificados_100')
    #     self.assertEqual(200 , request.status_code)

    # @requests_mock.Mocker()
    # def test_update_twitter_accounts(self, request_mock):
    #     url = (f"https://api.twitter.com/2/users/by?usernames={usernames_to_found}&user.fields=verified,url")
    #     data = { }
    #     data_expected = 'Done. Use url api/get_all_deputies for get all the deputies in db'

    #     request_mock.get(url, json=data)
    #     request = self.client.get('/api/update_twitter_accounts')
    #     self.assertEqual(200 , request.status_code)
    #     self.assertEqual(data_expected , request.data.decode())

    def test_api_update_tweets(self):
        data_expected = 'Updated tweets sucessfully. Now use /get_all_tweets to see the tweets'

        request = self.client.get('/api/update_tweets')
        self.assertEqual(data_expected , request.data.decode())

    def test_get_all_deputies_status(self):
        request = self.client.get('/api/get_all_deputies')
        self.assertEqual(200 , request.status_code)

    def test_get_all_tweets_status(self):
        request = self.client.get('/api/get_all_tweets')
        self.assertEqual(200 , request.status_code)

    def test_api_delete_all_tweets_propositions(self):
        data_expected = 'All propositions tweets were deleted'

        request = self.client.get('/api/delete_all_tweets_propositions')
        self.assertEqual(data_expected , request.data.decode())

    def test_api_get_all_tweets_propositions(self):
        data_not_expected = []

        request = self.client.get('/api/get_all_tweets_propositions')
        self.assertEqual(200 , request.status_code)
        self.assertNotEqual(data_not_expected , request.data.decode())

    def test_api_update_tweets_propositions(self):
        data_expected = 'Done'

        request = self.client.get('/api/update_tweets_propositions')
        self.assertEqual(data_expected , request.data.decode())

    def test_get_all_propositions_status(self):
        request = self.client.get('/api/get_all_propositions')
        self.assertEqual(200 , request.status_code)

    def test_delete_all_tweets_status(self):
        data_expected = 'All tweets were deleted'

        request = self.client.get('/api/delete_all_tweets')
        self.assertEqual(data_expected , request.data.decode())
    
    def tearDown(self):
        self.context.pop()


if __name__=='__main__':
    unittest.main()
