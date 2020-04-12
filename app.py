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
        return redirect('/dashboard')

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
    @app.route('/dashboard')
    @requires_auth
    def dashboard():
        return render_template('dashboard.html',
                               userinfo=session['profile'],
                               userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

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


    # Insert records so we can test our class methods and db
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
          "Saturday": "12:00 pm - 4:00 pm, 5:30 pm - 12:00 am",
          "Sunday": "12:00 pm - 4:00 pm, 5:30 pm - 11:00 pm"
        })
    chinese.insert()

    my_review = Review(
        restaurant_id = 1,
        name = "Morgan",
        date = datetime.today(),
        rating = 4,
        comments = "This place is a blast.")
    my_review.insert()

    ## ENDPOINTS

    '''
    GET /restaurants
        It should be a public endpoint.
        It should contain only the Restaurant.short() data representation.
        On success, this endpoint returns status code 200 and
        json {"success": True, "restaurants": restaurants}
        where restaurants is the list of restaurants.
        On failure, it aborts with a 404 error code.
    '''
    @app.route('/restaurants')
    def get_restaurants():
        try:
            restaurants = Restaurant.query.all()
            restaurants_short = []
            if len(restaurants) != 0:
                for restaurant in restaurants:
                    # We need to replace all single quotes with double quotes in
                    # order to make the data valid as a JSON string.
                    # restaurant.latlng = restaurant.latlng.replace("\'", "\"")
                    restaurants_short.append(restaurant.short())

            return jsonify({
                    "success": True,
                    "restaurants": restaurants_short
                })

        except Exception:
            abort(404)

    '''
    GET /restaurants/<id>
        It should be a public endpoint.
        It should contain only the Restaurant.long() data representation.
        On success, this endpoint returns status code 200 and
        json {"success": True, "restaurant": restaurant}
        where restaurant is the restaurant with the id requested.
        On failure, it aborts with a 404 error code.
    '''
    @app.route('/restaurants/<int:id>')
    def get_restaurant(id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        db_response = ' '
        if restaurant == None:
            abort(404)

        return render_template('restaurant.html',
                                   restaurant=restaurant.long(),
                                   success=True,
                                   domain=os.getenv("APP_DOMAIN"))

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
