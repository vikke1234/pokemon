from application import app, db
from flask import render_template, request, redirect, url_for
from application.pokemon.models import Pokemon


@app.route("/pokemon", methods=["GET"])
def pokemon_index():
    return render_template("pokemon/list.html", pokemon=Pokemon.query.all())


@app.route("/pokemon/new")
def poke_form():
    return render_template("pokemon/new.html")


@app.route("/pokemon", methods=["POST"])
def create_pokemon():
    _type = request.form.get("type")
    name = request.form.get("name")
    print(request)
    print("name: " + name + ", type: " + _type)
    p = Pokemon(name, _type)

    db.session.add(p)
    db.session.commit()
    return redirect(url_for("pokemon_index"))
