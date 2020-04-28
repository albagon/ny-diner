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
        self.user_type = os.environ['USER_TYPE']

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
        u_type = user.upper()
        if u_type == 'DINER':
            token = os.environ['TOKEN_DINER']
        elif u_type == 'RESTAURATEUR':
            token = os.environ['TOKEN_RESTAURATEUR']
        elif u_type == 'NYDINER_ADMIN':
            token = os.environ['TOKEN_NYDINER_ADMIN']
        else:
            token = ''
        return token

    """
    For each endpoint in the app, write at least:
        - one test for successful operation
        - one test for expected errors
    And for each user-role in Auth0, write at least 2 tests.
    """
    #Tests for GET /restaurants endpoint
    def test_get_restaurants(self):
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().get('/restaurants', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_restaurants'])
        self.assertTrue(len(data['restaurants']))

    def test_404_if_route_does_not_exist(self):
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().get('/restaurant', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #Tests for GET /restaurants/<id> endpoint
    def test_get_restaurant_by_id(self):
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().get('/restaurants/1', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['restaurant'])
        self.assertTrue(data['reviews'])

    def test_404_if_restaurant_does_not_exist(self):
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().get('/restaurants/100', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #Tests for POST /restaurants/<id>/new_reviews endpoint
    def test_create_new_review(self):
        new_review = {
        	"name": "Steph",
            "rating": 4,
            "comments": "Five star food, two star atmosphere. I would definitely get takeout from this place - but dont think I have the energy to deal with the hipster ridiculousness again. By the time we left the wait was two hours long."
        }
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().post('/restaurants/1/new_reviews', headers={'Authorization': f'Bearer {token}'}, json=new_review)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['review'])

    def test_422_if_wrong_restaurant_id(self):
        new_review = {
        	"name": "Steph",
            "rating": 4,
            "comments": "Five star food, two star atmosphere. I would definitely get takeout from this place - but dont think I have the energy to deal with the hipster ridiculousness again. By the time we left the wait was two hours long."
        }
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().post('/restaurants/111/new_reviews', headers={'Authorization': f'Bearer {token}'}, json=new_review)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    #Tests for POST /new_restaurants endpoint
    def test_create_new_restaurant(self):
        new_restaurant = {
            "name": "Mission Chinese Food2",
            "borough": "Manhattan",
            "photograph": "https://cdn.shopify.com/s/files/1/0734/9587/files/cafe_2048x2048.jpg?11619187030533083668",
            "img_description": "An inside view of a busy restaurant with all tables ocupied by people enjoying their meal",
            "address": "171 E Broadway, New York, NY 10002",
            "latlng": {
              "lat": 40.713829,
              "lng": -73.989667
            },
            "cuisine": "Chinese",
            "operating_hours": {
              "Monday": "5:30 pm - 11:00 pm",
              "Tuesday": "5:30 pm - 12:00 am",
              "Wednesday": "5:30 pm - 12:00 am",
              "Thursday": "5:30 pm - 12:00 am",
              "Friday": "5:30 pm - 12:00 am",
              "Saturday": "12:00 pm - 4:00 pm",
              "Sunday": "12:00 pm - 4:00 pm"
            }
        }
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().post('/new_restaurants', headers={'Authorization': f'Bearer {token}'}, json=new_restaurant)
        data = json.loads(res.data)

        if os.environ['USER_TYPE'] == 'DINER':
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unauthorized')
        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['restaurant'])

    def test_create_new_restaurant_without_data(self):
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().post('/new_restaurants', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        if os.environ['USER_TYPE'] == 'DINER':
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unauthorized')
        else:
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unprocessable')

    #Tests for PATCH /restaurants/<id> endpoint
    def test_patch_restaurant(self):
        new_restaurant = {
            "name": "Mission Chinese Food5",
            "borough": "Manhattan",
            "photograph": "https://cdn.shopify.com/s/files/1/0734/9587/files/cafe_2048x2048.jpg?11619187030533083668",
            "img_description": "An inside view of a busy restaurant with all tables ocupied by people enjoying their meal",
            "address": "171 E Broadway, New York, NY 10002",
            "latlng": {
              "lat": 40.713829,
              "lng": -73.989667
            },
            "cuisine": "Chinese",
            "operating_hours": {
              "Monday": "5:30 pm - 11:00 pm",
              "Tuesday": "5:30 pm - 12:00 am",
              "Wednesday": "5:30 pm - 12:00 am",
              "Thursday": "5:30 pm - 12:00 am",
              "Friday": "5:30 pm - 12:00 am",
              "Saturday": "12:00 pm - 4:00 pm",
              "Sunday": "12:00 pm - 4:00 pm"
            }
        }
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().patch('/restaurants/1', headers={'Authorization': f'Bearer {token}'}, json=new_restaurant)
        data = json.loads(res.data)

        if os.environ['USER_TYPE'] == 'DINER':
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unauthorized')
        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['restaurant'])

    def test_404_if_patch_wrong_restaurant_id(self):
        new_restaurant = {
            "name": "Mission Chinese Food5",
            "borough": "Manhattan",
            "photograph": "https://cdn.shopify.com/s/files/1/0734/9587/files/cafe_2048x2048.jpg?11619187030533083668",
            "img_description": "An inside view of a busy restaurant with all tables ocupied by people enjoying their meal",
            "address": "171 E Broadway, New York, NY 10002",
            "latlng": {
              "lat": 40.713829,
              "lng": -73.989667
            },
            "cuisine": "Chinese",
            "operating_hours": {
              "Monday": "5:30 pm - 11:00 pm",
              "Tuesday": "5:30 pm - 12:00 am",
              "Wednesday": "5:30 pm - 12:00 am",
              "Thursday": "5:30 pm - 12:00 am",
              "Friday": "5:30 pm - 12:00 am",
              "Saturday": "12:00 pm - 4:00 pm",
              "Sunday": "12:00 pm - 4:00 pm"
            }
        }
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().patch('/restaurants/133', headers={'Authorization': f'Bearer {token}'}, json=new_restaurant)
        data = json.loads(res.data)

        if os.environ['USER_TYPE'] == 'DINER':
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unauthorized')
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')

    #Tests for DELETE /restaurants/<id> endpoint
    def test_delete_restaurant(self):
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().delete('/restaurants/1', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        if os.environ['USER_TYPE'] == 'DINER' or os.environ['USER_TYPE'] == 'RESTAURATEUR':
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unauthorized')
        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['delete'])
            self.assertTrue(data['name'])

    def test_404_if_delete_wrong_restaurant_id(self):
        token = NydinerTestCase.get_access_token(self.user_type)
        res = self.client().delete('/restaurants/134', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)

        if os.environ['USER_TYPE'] == 'DINER' or os.environ['USER_TYPE'] == 'RESTAURATEUR':
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unauthorized')
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
