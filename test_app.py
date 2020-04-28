import os
import unittest
import json
from flask import jsonify
from urllib.parse import urlencode
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Restaurant, Review
from data import populate_db


class NydinerTestCase(unittest.TestCase):
    """This class represents the NY Diner test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        config = {
            'test_config': {
                'database_path': os.environ['DATABASE_TEST_URL']
            }
        }
        self.app = create_app(**config)
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.app.db.create_all()

        populate_db()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            self.app.db.drop_all()

    @staticmethod
    def get_access_token(user=None):
        """
        Get a token for the user requested
        The user can be: NYDINER_ADMIN, RESTAURATEUR or DINER
        """
        user_type = user.upper()
        if user == 'NYDINER_ADMIN':
            token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlF6VkNNMFJDTjBNeE56TXpSa0l4TmtZeE5UWkJRME0wTmpneE5rUTRORU0xTXpORE56azJRUSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNjRlMWQ3MzIwYzEyMGQ0M2U3MmJjZSIsImF1ZCI6InJlc3RhdXJhbnRzIiwiaWF0IjoxNTg4MDgxNjgyLCJleHAiOjE1ODgwODg4ODIsImF6cCI6ImFsbnl1ZkxGbGNXSUdreUZQaThUdDNRbFc0NE94YldWIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpyZXN0YXVyYW50cyIsInBvc3Q6cmVzdGF1cmFudHMiLCJwb3N0OnJldmlld3MiXX0.EHWNC5ZMCKNYp5jNUnJIQgPpcXTSukmvatrAaaQIvqcIFQXOYsX9dQ9dao-REUhV3YuVcdKCEcbK3aaLR0DL4VrrMDp4eDS8OXve9_u42wrph_oPKkwHsadNDfV12vdSJBIIoTe1TZ0GqRerSp3L3qFztQXKz5fcmEGnotVowg26pZDhjVM4y1nQXJaGBV18us-zW5VEwmS5b9E_CKpQVcTSshzavrIVTfXefWEYTU5eCRdVcreNEEaqdYf_maBVCVBzSlC79DpSvoAqZrSaG9RdoZR3jE0uhD-7OojbDcnEbdxj8EYZ10WU2i25qxn6qvHC7xex25n7LMVzeQ5PhA'
        elif user == 'DINER':
            token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlF6VkNNMFJDTjBNeE56TXpSa0l4TmtZeE5UWkJRME0wTmpneE5rUTRORU0xTXpORE56azJRUSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOGYzNjViOTM3NDA1MGMwYjk4NGVlZiIsImF1ZCI6InJlc3RhdXJhbnRzIiwiaWF0IjoxNTg4MDg2MjI3LCJleHAiOjE1ODgwOTM0MjcsImF6cCI6ImFsbnl1ZkxGbGNXSUdreUZQaThUdDNRbFc0NE94YldWIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6cmVzdGF1cmFudHMiLCJwb3N0OnJldmlld3MiXX0.i_zJ7T0WUtVMS6vE1h9TUoNtgU6NzNTyrhHfc6neWTbxpjjwoa0SR3Ka8THW6Wbt0tkuPkqG3vM__V6zj69_CjofuDsLQwvPFiDVbtHDGMvGApLUTGAzB86FxrPq3y-meU0ZGc3C9y7qfcnqvD98pRhuhcTS43q0NS3VkTzAlTrvKUN-9xrik2S6zyHxOlCAEjvv8Dkey1_W7qz_kcpeLK5aU2lLFrudHjV8JlmCIpszR-Mn_XaYGDrKBmf8FlW-0FNIHWxs9ZXLbzs4JQpWwx70FKctdZ6DOC90oupLjAs2s9ZzWWg10q-4ce5CbTmgMEVfDlNnGxQn8sgvj4yo4w'
        else:
            token = ''
        return token

    """
    For each endpoint in the app, write at least:
        - one test for successful operation
        - one test for expected errors
    And for each user-role in Auth0, write at least 2 tests.
    """
    #Endpoints for GET /restaurants
    def test_get_restaurants(self):
        token = NydinerTestCase.get_access_token('DINER')
        res = self.client().get('/restaurants', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_restaurants'])
        self.assertTrue(len(data['restaurants']))

    def test_404_if_route_does_not_exist(self):
        token = NydinerTestCase.get_access_token('DINER')
        res = self.client().get('/restaurant', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #Endpoints for GET /restaurants/<id>
    def test_get_restaurant_by_id(self):
        token = NydinerTestCase.get_access_token('NYDINER_ADMIN')
        res = self.client().get('/restaurants/1', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['restaurant'])
        self.assertTrue(data['reviews'])

    def test_404_if_restaurant_does_not_exist(self):
        token = NydinerTestCase.get_access_token('NYDINER_ADMIN')
        res = self.client().get('/restaurants/100', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
