from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from os import urandom
import os
app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokemon.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.pokemon import models
from application.pokemon import views

from application.auth import models
from application.auth import views

from application.auth.models import User
app.config["SECRET_KEY"] = urandom(32)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from application.pokemon.models import Pokemon

try:
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        db.session.add(
            User("admin", "admin", flask_bcrypt.generate_password_hash("123")))
        db.session.add(Pokemon("Pikatchu", "electric", "-", False))
        db.session.commit()
except:
    pass
