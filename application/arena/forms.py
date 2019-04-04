from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, TextField, validators


class NewArena(FlaskForm):
    name = StringField("Arena name", [validators.Length(min=1, max=10)])
    custom_allowed = BooleanField("Custom allowed")
    unranked = BooleanField("Ranked")
    description = TextField("Description")
    prize = IntegerField("Prize", [validators.NumberRange(min=0)])

    class Meta:
        csrf = False
