from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, AnyOf, URL, NumberRange
from enums import Borough, Cuisine, Hour

class ReviewForm(Form):
    restaurant_id = StringField(
        'restaurant_id', validators=[DataRequired()]
    )
    name = StringField(
        'name', validators=[DataRequired()]
    )
    date = DateTimeField(
        'date',
        validators=[DataRequired()],
        default= datetime.today()
    )
    rating = SelectField(
        'rating', validators=[DataRequired()],
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    )
    comments = TextAreaField(
        'comments', validators=[DataRequired()]
    )

class RestaurantForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    borough = SelectField(
        'borough', validators=[DataRequired()],
        choices=Borough.getBoroughs()
    )
    photograph = StringField(
        'photograph', validators=[DataRequired()]
    )
    img_description = StringField(
        'img_description', validators=[DataRequired()]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    lat = DecimalField(
        'lat', validators=[DataRequired(), NumberRange(min=-90, max=90)],
        places=6
    )
    lng = DecimalField(
        'lng', validators=[DataRequired(), NumberRange(min=-180, max=180)],
        places=6
    )
    cuisine = SelectField(
        'cuisine', validators=[DataRequired()],
        choices=Cuisine.getCuisines()
    )
    mon_st = SelectField(
        'mon_st', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    mon_cl = SelectField(
        'mon_cl', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    tue_st = SelectField(
        'tue_st', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    tue_cl = SelectField(
        'tue_cl', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    wed_st = SelectField(
        'wed_st', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    wed_cl = SelectField(
        'wed_cl', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    thu_st = SelectField(
        'thu_st', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    thu_cl = SelectField(
        'thu_cl', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    fri_st = SelectField(
        'fri_st', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    fri_cl = SelectField(
        'fri_cl', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    sat_st = SelectField(
        'sat_st', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    sat_cl = SelectField(
        'sat_cl', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    sun_st = SelectField(
        'sun_st', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    sun_cl = SelectField(
        'sun_cl', validators=[DataRequired()],
        choices=Hour.getHours()
    )
