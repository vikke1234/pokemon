from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=144)])
    password = PasswordField("Password", [validators.Length(min=3, max=144)])

    class Meta:
        csrf = False


class RegisterForm(FlaskForm):
    name = StringField("Name")
    username = StringField("Username", [validators.Length(min=3, max=144)])
    password = PasswordField("Password", [validators.Length(min=3, max=144)])

    class Meta:
        csrf = False
