import os
import unittest
import json
from flask import jsonify
from urllib.parse import urlencode
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Restaurant, Review


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
        else:
            token = ''
        return token

    """
    Write at least one test for each test for successful operation and for
    expected errors.
    """

    def test_get_restaurant_by_id(self):
        token = NydinerTestCase.get_access_token('NYDINER_ADMIN')
        one = Restaurant(
            name = "Mission Chinese Food",
            borough = "Manhattan",
            photograph = "https://cdn.shopify.com/s/files/1/0734/9587/files/cafe_2048x2048.jpg?11619187030533083668",
            img_description = "An inside view of a busy restaurant with all tables ocupied by people enjoying their meal",
            address = "171 E Broadway, New York, NY 10002",
            latlng = [40.713829, -73.989667],
            cuisine = "Chinese",
            operating_hours = {
              "Monday": "17 - 23 hrs",
              "Tuesday": "17 - 23 hrs",
              "Wednesday": "17 - 23 hrs",
              "Thursday": "17 - 23 hrs",
              "Friday": "17 - 23 hrs",
              "Saturday": "12 - 16 hrs",
              "Sunday": "12 - 16 hrs"
            })
        one.insert()
        res = self.client().get('/restaurants/1', headers={'Authorization': f'Bearer {token}'})
        data = json.loads(res.data)
        print('this is the data', data)

        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
