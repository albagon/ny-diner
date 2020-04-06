import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()


'''
Restaurants
This table holds the information of all participating restaurants
'''
class Restaurant(db.Model):
  __tablename__ = 'Restaurants'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  borough = Column(String, nullable=False)
  photograph = Column(String, nullable=False)
  img_description = Column(String, nullable=False)
  address = Column(String, nullable=False)
  latlng = Column(String, nullable=False)
  cuisine = Column(String, nullable=False)
  operating_hours = Column(String, nullable=False)

  def __init__(self, name, borough, photograph, img_description, address, latlng, cuisine, operating_hours):
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
Reviews
This table holds the information of all the reviews made to all restaurants
'''
class Review(db.Model):
  __tablename__ = 'Reviews'

  id = Column(Integer, primary_key=True)
  restaurant_id = Column(Integer)
  name = Column(String, nullable=False)
  date = Column(Date, nullable=False)
  rating = Column(Integer, nullable=False)
  comments = Column(String, nullable=False)

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
