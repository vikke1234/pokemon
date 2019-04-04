from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.pokemon.models import Pokemon
from application.pokemon.forms import PokeForm
from application.auth.models import User


@app.route("/pokemon", methods=["GET"])
@login_required
def pokemon_index():
    return render_template(
        "pokemon/list.html",
        pokemon=Pokemon.query.filter(
            User.id == current_user.get_id()))


@app.route("/pokemon/new")
@login_required
def poke_form():
    return render_template("pokemon/new.html", form=PokeForm())


@app.route("/pokemon/<poke_id>/", methods=["GET"])
@login_required
def get_pokemon(poke_id):
    p = Pokemon.query.get(int(poke_id))
    return render_template("pokemon/specific.html", pokemon=p)


@app.route("/pokemon", methods=["POST"])
@login_required
def create_pokemon():
    form = PokeForm(request.form)
    name = form.name.data
    _type = form.poke_type.data
    description = form.description.data
    custom = form.custom.data
    p = Pokemon(name, _type, description, custom, current_user.get_id())

    db.session.add(p)
    db.session.commit()
    return redirect(url_for("pokemon_index"))


@app.route("/pokemon/<poke_id>/edit/", methods=["GET", "POST"])
@login_required
def edit_pokemon(poke_id):
    p = Pokemon.query.get(int(poke_id))
    if (request.method == "GET"):
        return render_template("pokemon/edit.html", form=PokeForm(), pokemon=p)
    form = PokeForm(request.form)
    p.name = form.name.data
    p.poke_type = form.poke_type.data
    p.custom = form.custom.data
    p.description = form.description.data
    db.session.commit()
    return render_template("pokemon/specific.html", pokemon=p)
