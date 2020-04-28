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
from auth import AuthError, requires_auth_p

def create_app(test_config = None):
    # Load environment variables from dot env file.
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("AUTH0_CLIENT_SECRET")
    setup_db(app)

    # Allow CORS for all domains on all routes
    CORS(app)
    db_drop_and_create_all()

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
        session['profile'] = {
            'user_id': "userinfo['sub']",
            'name': "Diner",
            'picture': "userinfo['picture']"
        }
        return render_template('catcher.html')

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
    def index():
        link = ('https://'+ os.getenv("AUTH0_DOMAIN")
                + '/authorize?audience=' + os.getenv("AUTH0_AUDIENCE")
                + '&response_type=token&client_id=' + os.getenv("AUTH0_CLIENT_ID")
                + '&redirect_uri=' + os.getenv("AUTH0_CALLBACK_URL"))
        return render_template('index.html', link=link)

    # Log the user out and clear the data from the session.
    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        params = {'returnTo': url_for('index', _external=True), 'client_id': os.getenv("AUTH0_CLIENT_ID")}
        return redirect('https://' + os.getenv("AUTH0_DOMAIN") + '/v2/logout?' + urlencode(params))

    '''
    ENDPOINTS for Restaurants and Reviews
    '''

    '''
    GET /restaurants
        It requires 'get:restaurants' permission.
        It should contain only the Restaurant.short() data representation.
        On success, this endpoint returns status code 200, the list of
        restaurants and the total number of restaurants. On failure, it aborts
        with a 404 error code.
    '''
    @app.route('/restaurants')
    @requires_auth_p('get:restaurants')
    def get_restaurants(payload):
        try:
            restaurants = Restaurant.query.all()
            restaurants_short = []
            if len(restaurants) != 0:
                any_restaurants = True
                for restaurant in restaurants:
                    restaurants_short.append(restaurant.short())
            return jsonify({
                'success': True,
                'restaurants': restaurants_short,
                'total_restaurants': len(restaurants_short)
            })
        except Exception:
            abort(404)

    '''
    GET /restaurants/<id>
        It requires 'get:restaurants' permission.
        It should contain the Restaurant.long() data representation.
        On success, this endpoint returns status code 200, the restaurant data,
        and a list of reviews on that restaurant.
        On failure, it aborts with a 404 error code.
    '''
    @app.route('/restaurants/<int:id>')
    @requires_auth_p('get:restaurants')
    def get_restaurant(payload, id):
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

                return jsonify({
                    'success': True,
                    'restaurant': restaurant.long(),
                    'reviews': reviews_format
                })
        except Exception:
            abort(404)

    '''
    POST /restaurants/<id>/new_reviews
        Post a new review in db.
    '''
    @app.route('/restaurants/<int:id>/new_reviews', methods=['POST'])
    @requires_auth_p('post:reviews')
    def create_review_submission(payload, id):
        error = False
        try:
            body = request.get_json()
            review = Review(
                restaurant_id = id,
                name = body.get('name', ''),
                date = datetime.now(),
                rating = body.get('rating', 1),
                comments = body.get('comments', '')
            )
            review.insert()
            new_review = Review.query.filter(Review.id == review.id).one_or_none()
            if new_review != None:
                new_review_f = new_review.format()
            else:
                error = True
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if not error:
            # on successful db insert, print success
            print('Success post review')
            return jsonify({
                'success': True,
                'review': new_review_f
            })
        else:
            print('An error occurred. Review could not be listed.')
            abort(422)

    '''
    POST /new_restaurants
        Post a new restaurant in db.
    '''
    @app.route('/new_restaurants', methods=['POST'])
    @requires_auth_p('post:restaurants')
    def create_restaurant_submission(payload):
        error = False
        try:
            body = request.get_json()
            latlng = body.get('latlng', {"lat":40, "lng":-73})
            restaurant = Restaurant(
                name = body.get('name', ''),
                borough = body.get('borough', ''),
                photograph = body.get('photograph', ''),
                img_description = body.get('img_description', ''),
                address = body.get('address', ''),
                latlng = [float(latlng['lat']), float(latlng['lng'])],
                cuisine = body.get('cuisine', ''),
                operating_hours = body.get('operating_hours', {})
                )
            restaurant.insert()
            new_restaurant = Restaurant.query.filter(Restaurant.id == restaurant.id).one_or_none()
            if new_restaurant != None:
                new_restaurant_f = restaurant.long()
            else:
                error = True
        except:
            error = True
            print('The restaurant could not be listed.')
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if not error:
            print('Restaurant was successfully listed.')
            return jsonify({
                'success': True,
                'restaurant': new_restaurant_f
            })
        else:
            print('An error occurred. Restaurant could not be listed.')
            abort(422)

    '''
    PATCH /restaurants/<id>
        Where <id> is the existing model id.
        It should respond with a 404 error if <id> is not found.
        It should update the corresponding row for <id>
        It should require the 'patch:restaurants' permission.
        It should contain the restaurant.long() data representation.
    '''
    @app.route('/restaurants/<int:id>', methods=['PATCH'])
    @requires_auth_p('patch:restaurants')
    def update_restaurant(payload, id):
        error = False
        try:
            body = request.get_json()
            restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
            if restaurant != None:
                latlng = body.get('latlng', {"lat":40, "lng":-73})
                restaurant.name = body.get('name', '')
                restaurant.borough = body.get('borough', '')
                restaurant.photograph = body.get('photograph', '')
                restaurant.img_description = body.get('img_description', '')
                restaurant.address = body.get('address', '')
                restaurant.latlng[0] = float(latlng['lat'])
                restaurant.latlng[1] = float(latlng['lng'])
                restaurant.cuisine = body.get('cuisine', '')
                restaurant.operating_hours = body.get('operating_hours', {})
                restaurant.update()
            else:
                abort(404)
        except Exception:
            error = True
            message = 'The restaurant could not be updated.'
            db.session.rollback()
            print(sys.exc_info())
        if not error:
            print('Restaurant was successfully updated.')
            return jsonify({
                        "success": True,
                        "restaurant": restaurant.long()
                    })
        else:
            print('An error occurred. Restaurant not updated.')
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
