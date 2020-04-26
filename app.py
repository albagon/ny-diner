from functools import wraps
import json
import os
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, redirect, render_template, session, url_for, abort, flash, request
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from datetime import datetime
import sys

from models import db, setup_db, db_drop_and_create_all, Restaurant, Review
from data import populate_db
from forms import *

# Load environment variables from dot env file.
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("AUTH0_CLIENT_SECRET")
setup_db(app)

# Allow CORS for all domains on all routes
CORS(app)
db_drop_and_create_all()

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
INSERT records into db
'''
populate_db()

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
ENDPOINTS for Restaurants and Reviews
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
    and a list of reviews on that restaurant.
    On failure, it aborts with a 404 error code.
    This route also returns the user information stored in the Flask session.
'''
@app.route('/restaurants/<int:id>')
@requires_auth
def get_restaurant(id):
    try:
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        if restaurant != None:
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
                                       form=restaurant.to_form())
    except Exception:
        abort(404)

'''
GET /restaurants/<id>/new_reviews
    Renders the template associated with the new_review form.
'''
@app.route('/restaurants/<int:id>/new_reviews', methods=['GET'])
@requires_auth
def create_review_form(id):
    try:
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        if restaurant != None:
            form = ReviewForm()
            return render_template('forms/new_review.html',
                                     userinfo=session['profile'],
                                     restaurant=restaurant,
                                     form=form)
        else:
            abort(404)
    except Exception:
        abort(404)

'''
POST /restaurants/<id>/new_reviews
    Post a new review in db.
'''
@app.route('/restaurants/<int:id>/new_reviews', methods=['POST'])
@requires_auth
def create_review_submission(id):
    error = False
    body = {}
    try:
        form = request.form
        review = Review(
            restaurant_id = id,
            name = form['name'],
            date = datetime.now(),
            rating = form['rating'],
            comments = form['comments']
        )
        review.insert()
        body['name'] = form['name']
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Thank you ' + body['name'] + ' for your review.', 'success')
    else:
        flash('An error occurred. Review could not be listed.', 'error')
    return redirect('/restaurants/'+str(id)+'/new_reviews')

'''
GET /new_restaurants
    Renders the template associated with the new_restaurant form.
'''
@app.route('/new_restaurants', methods=['GET'])
@requires_auth
def create_restaurant_form():
    try:
        form = RestaurantForm()
        return render_template('forms/new_restaurant.html',
                                 userinfo=session['profile'],
                                 form=form)
    except Exception:
        abort(404)

'''
POST /new_restaurants
    Post a new restaurant in db.
'''
@app.route('/new_restaurants', methods=['POST'])
@requires_auth
def create_restaurant_submission():
    error = False
    try:
        form = RestaurantForm(request.form)
        if form.validate_on_submit():
            op_hours = format_operating_hours(form)
            if op_hours['success']:
                restaurant = Restaurant(
                    name = form.name.data,
                    borough = form.borough.data,
                    photograph = form.photograph.data,
                    img_description = form.img_description.data,
                    address = form.address.data,
                    latlng = [float(form.lat.data), float(form.lng.data)],
                    cuisine = form.cuisine.data,
                    operating_hours = op_hours['week_hours']
                    )
                restaurant.insert()
            else:
                error = True
                message = 'Wrong formating of operating hours.'
        else:
            error = True
            message = 'The form contains invalid data.'
    except:
        error = True
        message = 'The restaurant could not be listed.'
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        flash(form.name.data + ' was successfully listed.', 'success')
        return redirect('/new_restaurants')
    else:
        flash('An error occurred. ' + message, 'error')
        return render_template('forms/new_restaurant.html',
                                 userinfo=session['profile'],
                                 form=form)

'''
PATCH /restaurants/<id>
    Where <id> is the existing model id.
    It should respond with a 404 error if <id> is not found.
    It should update the corresponding row for <id>
    It should require the 'patch:restaurants' permission.
    It should contain the restaurant.long() data representation.
'''
@app.route('/restaurants/<int:id>', methods=['PATCH'])
@requires_auth
def update_restaurant(id):
    error = False
    try:
        form = RestaurantForm(request.form)
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        if restaurant != None:
            if form.validate_on_submit():
                op_hours = format_operating_hours(form)
                if op_hours['success']:
                    restaurant.name = form.name.data,
                    restaurant.borough = form.borough.data,
                    restaurant.photograph = form.photograph.data,
                    restaurant.img_description = form.img_description.data,
                    restaurant.address = form.address.data,
                    restaurant.latlng[0] = float(form.lat.data),
                    restaurant.latlng[1] = float(form.lng.data),
                    restaurant.cuisine = form.cuisine.data,
                    restaurant.operating_hours = op_hours['week_hours']
                    restaurant.update()
                else:
                    error = True
                    message = 'Wrong formating of operating hours.'
            else:
                error = True
                message = 'The form contains invalid data.'
        else:
            abort(404)
    except Exception:
        error = True
        message = 'The restaurant could not be updated.'
        db.session.rollback()
        print(sys.exc_info())
    if not error:
        flash(form.name.data + ' was successfully updated.', 'success')
        return jsonify({
                    "success": True,
                    "restaurant": restaurant.long()
                })
    else:
        flash('An error occurred. ' + message, 'error')
        if form.errors:
            for field, f_errors in form.errors.items():
                if f_errors:
                    for error in f_errors:
                        flash(field + ': ' + error, 'error')
        abort(404)

'''
DELETE /restaurants/<id>
    Where <id> is the existing model id.
    It should respond with a 404 error if <id> is not found.
    It should delete the corresponding row for <id>
    It should require the 'delete:restaurants' permission.
    Returns status code 200 and json {"success": True, "delete": id,
    "name": restaurant.name} where id is the id of the deleted record or
    appropriate status code indicating reason for failure.
'''
@app.route('/restaurants/<int:id>', methods=['DELETE'])
@requires_auth
def delete_restaurant(id):
    try:
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        if restaurant != None:
            reviews = Review.query.filter(Review.restaurant_id == id).all()
            if len(reviews) != 0:
                for review in reviews:
                    review.delete()

            restaurant.delete()
            flash(restaurant.name + ' was successfully deleted.', 'success')
            return jsonify({
                    "success": True,
                    "delete": id,
                    "name": restaurant.name
                })
    except Exception:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. The restaurant could not be deleted.', 'error')
    return abort(404)

# Error handler for 401
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422
