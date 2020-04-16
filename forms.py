from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL

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
        choices=[(0, "1"), (1, "2"), (2, "3"), (3, "4"), (4, "5")]
    )
    comments = TextAreaField(
        'comments', validators=[DataRequired()]
    )
