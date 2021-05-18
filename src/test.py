import unittest
from app import app
from mongoengine import connect, disconnect
from flask import Flask
import requests_mock
import os

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

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('prlmntq_db_test', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()
    
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_get_tweets_status(self):
        request = self.client.get('/api/tweets')
        self.assertEqual(200 , request.status_code)

    def test_tweets_por_ids_status(self):
        request = self.client.get('/api/tweets_por_ids')
        self.assertEqual(200 , request.status_code)

    def test_update_twitter_accounts(self):
        data_expected = 'Done. Use url api/get_all_deputies for get all the deputies in db'

        request = self.client.get('/api/update_twitter_accounts')
        self.assertEqual(200 , request.status_code)
        self.assertEqual(data_expected , request.data.decode())
    

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

    def test_get_all_tweets_by_id_status(self):
        request = self.client.get('/api/get_tweets_id_deputy/3')
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

    def test_get_tweets_by_proposition_id_status(self):
        request = self.client.get('/api/get_tweets_by_proposition_id/3')
        self.assertEqual(200 , request.status_code)

    def tearDown(self):
        self.context.pop()


if __name__=='__main__':
    unittest.main()
