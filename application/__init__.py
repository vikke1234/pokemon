from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt

from os import urandom
import os
app = Flask(__name__)

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokemon.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

app.config["SECRET_KEY"] = urandom(32)

flask_bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

# roles in login_required
from functools import wraps


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False
            if role != "ANY":
                unauthorized = True
                roles = current_user.roles()
                if role in roles:
                    unauthorized = False

            if unauthorized:
                print("unauthorized")
                return login_manager.unauthorized()

            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


from application import views

from application.pokemon import models
from application.pokemon import views

from application.auth import models
from application.auth import views

from application.auth.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from application.pokemon.models import Pokemon, Move

try:
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        db.session.add(
            User("admin", "admin",
                 flask_bcrypt.generate_password_hash(os.environ.get("ADMIN_PASS").encode("utf-8"))))
        db.session.add(Pokemon("Pikatchu", "electric", "-", False))
        db.session.add(Move("Kick"))
        db.session.commit()
except:
    pass
