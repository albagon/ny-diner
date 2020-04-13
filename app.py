from functools import wraps
import json
import os
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, redirect, render_template, session, url_for, abort
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from datetime import datetime

from models import setup_db, Restaurant, Review

def create_app(test_config = None):

    app = Flask(__name__)

    # Load environment variables from dot env file.
    load_dotenv()

    app.secret_key = os.getenv("AUTH0_CLIENT_SECRET")

    '''
    Database settings
    '''
    setup_db(app)
    # Allow CORS for all domains on all routes
    CORS(app)

    '''
    Auth0 settings
    '''
    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id = os.getenv("AUTH0_CLIENT_ID"),
        client_secret = os.getenv("AUTH0_CLIENT_SECRET"),
        api_base_url = 'https://full.eu.auth0.com',
        access_token_url = 'https://full.eu.auth0.com/oauth/token',
        authorize_url = 'https://full.eu.auth0.com/authorize',
        client_kwargs = {
            'scope': 'openid profile email',
        },
    )

    '''
    Auth0 routes
    '''
    # Auth0 redirects the user to this route after they have authenticated.
    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/restaurants')

    # This route uses the Authlib client instance to redirect the user to the login page.
    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

    # Decorator that checks if the user has authenticated.
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                # Redirect to Login page here
                return redirect('/')
            return f(*args, **kwargs)

        return decorated

    # This route renders the user information stored in the Flask session.
    '''
    @app.route('/dashboard')
    @requires_auth
    def dashboard():
        return render_template('dashboard.html',
                               userinfo=session['profile'],
                               userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
    '''

    # This route renders once the user has logged out.
    @app.route('/')
    def home():
        return render_template('home.html')

    # Log the user out and clear the data from the session.
    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        params = {'returnTo': url_for('home', _external=True), 'client_id': os.getenv("AUTH0_CLIENT_ID")}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    '''
    INSERT records so we can test our class methods and db
    '''
    chinese = Restaurant(
        name = "Mission Chinese Food",
        borough = "Manhattan",
        photograph = "1.jpg",
        img_description = "An inside view of a busy restaurant with all tables ocupied by people enjoying their meal",
        address = "171 E Broadway, New York, NY 10002",
        latlng = [40.713829, -73.989667],
        cuisine = "Chinese",
        operating_hours = {
          "Monday": "5:30 pm - 11:00 pm",
          "Tuesday": "5:30 pm - 12:00 am",
          "Wednesday": "5:30 pm - 12:00 am",
          "Thursday": "5:30 pm - 12:00 am",
          "Friday": "5:30 pm - 12:00 am",
          "Saturday": "12:00 pm - 4:00 pm",
          "Sunday": "12:00 pm - 4:00 pm"
        })
    chinese.insert()

    korean = Restaurant(
        name = "Kang Ho Dong Baekjeong",
        borough = "Manhattan",
        photograph = "3.jpg",
        img_description = "An inside view of an empty restaurant. There is a steam pot in the middle of each table",
        address = "1 E 32nd St, New York, NY 10016",
        latlng = [40.747143, -73.985414],
        cuisine = "Korean",
        operating_hours = {
          "Monday": "11:30 am - 2:00 am",
          "Tuesday": "11:30 am - 2:00 am",
          "Wednesday": "11:30 am - 2:00 am",
          "Thursday": "11:30 am - 2:00 am",
          "Friday": "11:30 am - 6:00 am",
          "Saturday": "11:30 am - 6:00 am",
          "Sunday": "11:30 am - 2:00 am"
        })
    korean.insert()

    my_review = Review(
        restaurant_id = 1,
        name = "Morgan",
        date = datetime.today(),
        rating = 4,
        comments = "Mission Chinese Food has grown up from its scrappy Orchard Street days into a big, two story restaurant equipped with a pizza oven, a prime rib cart, and a much broader menu. Yes, it still has all the hits — the kung pao pastrami, the thrice cooked bacon —but chef/proprietor Danny Bowien and executive chef Angela Dimayuga have also added a raw bar, two generous family-style set menus, and showstoppers like duck baked in clay. And you can still get a lot of food without breaking the bank.")
    my_review.insert()

    second_review = Review(
        restaurant_id = 1,
        name = "Alba",
        date = datetime.today(),
        rating = 4,
        comments = "Mission Chinese Food has grown up from its scrappy Orchard Street days into a big, two story restaurant equipped with a pizza oven, a prime rib cart, and a much broader menu. Yes, it still has all the hits — the kung pao pastrami, the thrice cooked bacon —but chef/proprietor Danny Bowien and executive chef Angela Dimayuga have also added a raw bar, two generous family-style set menus, and showstoppers like duck baked in clay. And you can still get a lot of food without breaking the bank.")
    second_review.insert()

    '''
    ENDPOINTS
    '''

    '''
    GET /restaurants
        It requires authentication.
        It should contain only the Restaurant.short() data representation.
        On success, this endpoint returns status code 200 and the list of
        restaurants. On failure, it aborts with a 404 error code.
        This route also returns the user information stored in the Flask session.
    '''
    @app.route('/restaurants')
    @requires_auth
    def get_restaurants():
        try:
            restaurants = Restaurant.query.all()
            restaurants_short = []
            if len(restaurants) != 0:
                any_restaurants = True
                for restaurant in restaurants:
                    restaurants_short.append(restaurant.short())
            return render_template('dashboard.html',
                                       userinfo=session['profile'],
                                       userinfo_pretty=json.dumps(session['jwt_payload'], indent=4),
                                       success=True,
                                       restaurants=restaurants_short)
        except Exception:
            abort(404)

    '''
    GET /restaurants/<id>
        It should be a public endpoint.
        It should contain the Restaurant.long() data representation.
        On success, this endpoint returns status code 200, the restaurant data,
        a list of reviews on that restaurant and the APP_DOMAIN environment
        variable. On failure, it aborts with a 404 error code.
    '''
    @app.route('/restaurants/<int:id>')
    def get_restaurant(id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        if restaurant == None:
            abort(404)
        reviews = Review.query.filter(Review.restaurant_id == id).all()
        if len(reviews) != 0:
            reviews_format = []
            for review in reviews:
                reviews_format.append(review.format())
        else:
            reviews_format = False
        return render_template('restaurant.html',
                                   success=True,
                                   restaurant=restaurant.long(),
                                   reviews=reviews_format,
                                   domain=os.getenv("APP_DOMAIN"))


    return app

app = create_app()

if __name__ == '__main__':
    app.run()
