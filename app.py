import os
from flask import Flask, jsonify, abort
from flask_cors import CORS
from datetime import datetime
from models import setup_db, Restaurant, Review

def create_app(test_config = None):

    app = Flask(__name__)
    setup_db(app)
    # Allow CORS for all domains on all routes
    CORS(app)

    # Insert records so we can test our class methods and db
    chinese = Restaurant(
        name = "Mission Chinese Food",
        borough = "Manhattan",
        photograph = "1.jpg",
        img_description = "An inside view of a busy restaurant with all tables ocupied by people enjoying their meal",
        address = "171 E Broadway, New York, NY 10002",
        latlng = str({
          "lat": 40.713829,
          "lng": -73.989667
        }),
        cuisine = "Asian",
        operating_hours = str({
          "Monday": "5:30 pm - 11:00 pm",
          "Tuesday": "5:30 pm - 12:00 am",
          "Wednesday": "5:30 pm - 12:00 am",
          "Thursday": "5:30 pm - 12:00 am",
          "Friday": "5:30 pm - 12:00 am",
          "Saturday": "12:00 pm - 4:00 pm, 5:30 pm - 12:00 am",
          "Sunday": "12:00 pm - 4:00 pm, 5:30 pm - 11:00 pm"
        }))
    chinese.insert()

    my_review = Review(
        restaurant_id = 1,
        name = "Morgan",
        date = datetime.today(),
        rating = 4,
        comments = "This place is a blast.")
    my_review.insert()

    ## ROUTES

    @app.route('/')
    def index():
        healthy = os.environ['HEALTHY']
        if healthy == 'true': print("Super healthy!")
        return "Good progress!!"

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
                    restaurant.latlng = restaurant.latlng.replace("\'", "\"")
                    restaurant.operating_hours = restaurant.operating_hours.replace("\'", "\"")
                    restaurants_short.append(restaurant.short())

            return jsonify({
                    "success": True,
                    "restaurants": restaurants_short
                })

        except Exception:
            abort(404)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
