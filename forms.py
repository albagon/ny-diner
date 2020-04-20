from flask import abort
from datetime import datetime
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, AnyOf, URL, NumberRange
from enums import Borough, Cuisine, Hour

class ReviewForm(FlaskForm):
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

class RestaurantForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    borough = SelectField(
        'borough', validators=[DataRequired()],
        choices=Borough.getBoroughs()
    )
    photograph = StringField(
        'photograph', validators=[DataRequired(), URL()]
    )
    img_description = StringField(
        'img_description', validators=[DataRequired()]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    lat = DecimalField(
        'lat', validators=[DataRequired(), NumberRange(min=40.499080, max=40.913124)],
        places=6
    )
    lng = DecimalField(
        'lng', validators=[DataRequired(), NumberRange(min=-74.253449, max=-73.703058)],
        places=6
    )
    cuisine = SelectField(
        'cuisine', validators=[DataRequired()],
        choices=Cuisine.getCuisines()
    )
    opening_0 = SelectField(
        'opening_0', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    closing_0 = SelectField(
        'closing_0', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    opening_1 = SelectField(
        'opening_1', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    closing_1 = SelectField(
        'closing_1', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    opening_2 = SelectField(
        'opening_2', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    closing_2 = SelectField(
        'closing_2', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    opening_3 = SelectField(
        'opening_3', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    closing_3 = SelectField(
        'closing_3', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    opening_4 = SelectField(
        'opening_4', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    closing_4 = SelectField(
        'closing_4', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    opening_5 = SelectField(
        'opening_5', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    closing_5 = SelectField(
        'closing_5', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    opening_6 = SelectField(
        'opening_6', validators=[DataRequired()],
        choices=Hour.getHours()
    )
    closing_6 = SelectField(
        'closing_6', validators=[DataRequired()],
        choices=Hour.getHours()
    )

'''
Input: An opening time and a closing time. It checks that the opening time is earlier
that the closing time and returns a string with both values. If the opening time is
not earlier than closing time, it returns an error string.
It is also possible to receive "Closed" as an opening or closing time.
In this case the function returns "Closed".
'''
def create_hours(opening, closing):
    if ((opening == "Closed") | (closing == "Closed")):
        return "Closed"
    else:
        opening_time = int(opening)
        closing_time = int(closing)
        if (opening_time < closing_time):
            return opening + " - " + closing + " hrs"
        else:
            return "error"

'''
Input: A Restaurant Form.
Returns: A success equal to True and a dictionary with the operating hours of a Restaurant.
If the hours are not valid, then it returns a success equal to False.
'''
def format_operating_hours(form):
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week_hours = {}
    day_hours = ""
    form_dic = form.__dict__
    error = False
    for i, value in enumerate(week):
        day_hours = create_hours(form["opening_" + str(i)].data, form["closing_" + str(i)].data)
        if day_hours == "error":
            error = True
            break
        else:
            week_hours[value] = day_hours
    if error:
        operating_hours = {"success" : False, "week_hours": None}
    else:
        operating_hours = {"success" : True, "week_hours": week_hours}

    return operating_hours
