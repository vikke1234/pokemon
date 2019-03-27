from application import app, db
from flask import render_template, request, redirect, url_for
from application.pokemon.models import Pokemon
from application.pokemon.forms import PokeForm


@app.route("/pokemon", methods=["GET"])
def pokemon_index():
    return render_template("pokemon/list.html", pokemon=Pokemon.query.all())


@app.route("/pokemon/new")
def poke_form():
    return render_template("pokemon/new.html", form=PokeForm())


@app.route("/pokemon/<poke_id>/", methods=["GET"])
def get_pokemon(poke_id):
    p = Pokemon.query.get(int(poke_id))
    print(poke_id)
    return render_template("pokemon/specific.html", pokemon=p)


@app.route("/pokemon", methods=["POST"])
def create_pokemon():
    form = PokeForm(request.form)
    name = form.name.data
    _type = form.poke_type.data
    description = form.description.data
    custom = form.custom.data
    print(_type)
    p = Pokemon(name, _type, description, custom)

    db.session.add(p)
    db.session.commit()
    return redirect(url_for("pokemon_index"))
