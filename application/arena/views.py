from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import db, app
from models import Arena


@app.route("/arena")
def index():
    arenas = Arena.query.all()
    render_template("arena/list_of_arenas.html", arenas=arenas)
