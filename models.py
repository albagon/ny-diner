import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    Binds a flask application and a SQLAlchemy service.
'''
def setup_db(app, database_path = database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    '''
    Drop the database tables and start fresh
    Initialize a clean database
    '''
    db.drop_all()
    db.create_all()


'''
Restaurants
    This table holds the information of all participating restaurants.
'''
class Restaurant(db.Model):
    __tablename__ = 'Restaurants'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False, unique = True)
    borough = Column(String, nullable = False)
    photograph = Column(String, nullable = False)
    img_description = Column(String, nullable = False)
    address = Column(String, nullable = False)
    latlng = Column(String, nullable = False)
    cuisine = Column(String, nullable = False)
    operating_hours = Column(String, nullable = False)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)

    def __init__(self, name, borough, photograph, img_description, address,
                 latlng, cuisine, operating_hours):
        self.name = name
        self.borough = borough
        self.photograph = photograph
        self.img_description = img_description
        self.address = address
        self.latlng = latlng
        self.cuisine = cuisine
        self.operating_hours = operating_hours

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'borough': self.borough,
            'photograph': self.photograph,
            'img_description': self.img_description,
            'address': self.address,
            'latlng': self.latlng,
            'cuisine': self.cuisine,
            'operating_hours': self.operating_hours
        }

    '''
    insert()
        Inserts a new model into a database.
        The model must have a unique name.
        EXAMPLE
            chinese = Restaurant(
                name = "Mission Chinese Food",
                borough = "Manhattan",
                photograph = "1.jpg",
                img_description = "An inside view",
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
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        Deletes a model from a database.
        The model must exist in the database.
        EXAMPLE
            chinese.insert()
            chinese.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        Updates a model into a database.
        The model must exist in the database.
        EXAMPLE
            chinese = Restaurant.query.filter(Restaurant.id == id).one_or_none()
            chinese.name = "Local Chinese"
            chinese.update()
    '''
    def update(self):
        db.session.commit()

'''
Reviews
    This table holds the information of all the reviews made to all restaurants.
'''
class Review(db.Model):
    __tablename__ = 'Reviews'

    id = Column(Integer, primary_key = True)
    restaurant_id = Column(Integer, db.ForeignKey('Restaurants.id'), nullable = False)
    name = Column(String, nullable = False)
    date = Column(DateTime, nullable = False, default = datetime.today())
    rating = Column(Integer, nullable = False)
    comments = Column(String, nullable = False)

    def __init__(self, restaurant_id, name, date, rating, comments):
        self.restaurant_id = restaurant_id
        self.name = name
        self.date = date
        self.rating = rating
        self.comments = comments

    def format(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'date': self.date,
            'rating': self.rating,
            'comments': self.comments
        }

    '''
    insert()
        Inserts a new model into a database.
        EXAMPLE
            my_review = Review(
                restaurant_id = 1,
                name = "Morgan",
                rating = 4,
                comments = "This place is a blast.")
            my_review.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        Deletes a model from a database.
        The model must exist in the database.
        EXAMPLE
            my_review.insert()
            my_review.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()
