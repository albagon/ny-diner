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
from data import populate_db

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
    INSERT records so we can test our methods and db
    '''
    populate_db()

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
        This route also returns the user information stored in the Flask session.
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
                                   userinfo=session['profile'],
                                   restaurant=restaurant.long(),
                                   reviews=reviews_format,
                                   domain=os.getenv("APP_DOMAIN"))


    return app

app = create_app()

if __name__ == '__main__':
    app.run()
