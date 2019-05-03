from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.pokemon.models import Pokemon, Move
from application.pokemon.forms import PokeForm, DefaultPokemonForm
from application.pokemon.forms import Search, MoveForm
from application.auth.models import User


@app.route("/pokemon", methods=["GET", "POST"])
@login_required()
def pokemon_index():
    pokemon = Pokemon.get_user_pokemon(current_user.get_id())
    form = Search(request.form)
    if request.method == "POST":
        # filter when searching for pokemon
        pokemon = [p for p in pokemon if form.search.data in p.name.lower()]
    return render_template(
        "pokemon/list.html", pokemon=pokemon, search=Search())


@app.route("/pokemon/<int:poke_id>/", methods=["GET"])
@login_required()
def get_pokemon(poke_id):
    p = Pokemon.get_specific_pokemon(poke_id)
    moves = Move.query.join(Move.pokemon).filter_by(id=poke_id).join(
        Pokemon.accounts).filter_by(id=current_user.get_id()).all()

    return render_template(
        "pokemon/specific.html", pokemon=p, moves=moves, form=MoveForm())


@app.route("/pokemon/add_move/<int:poke_id>", methods=["POST"])
@login_required()
def add_move(poke_id):
    form = MoveForm(request.form)
    move = Move.query.filter_by(name=str(form.move_name.data)).first()
    p = Pokemon.get_specific_pokemon(poke_id)
    user = User.query.get(current_user.get_id())
    if p not in move.pokemon:
        move.pokemon.append(p)
    if user not in move.account \
       and Move.count_moves(poke_id, current_user.get_id()):
        move.account.append(user)

    db.session.add(move)
    db.session.commit()
    return redirect(url_for("get_pokemon", poke_id=poke_id))


@app.route("/pokemon/new", methods=["POST", "GET"])
@login_required(role="ADMIN")
def create_pokemon():
    form = PokeForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        _type = form.poke_type.data
        description = form.description.data
        custom = form.custom.data
        p = Pokemon(name, _type, description, custom)

        print("\033[93m" + "Pokemon" + "\033[0m")
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("pokemon_index"))
    return render_template("pokemon/new.html", form=PokeForm())


@app.route("/pokemon/remove/<int:poke_id>", methods=["POST", "GET"])
@login_required()
def remove_pokemon(poke_id):
    pokemon = Pokemon.get_specific_pokemon(poke_id)
    pokemon.accounts = [
        item for item in pokemon.accounts if item.id != current_user.get_id()
    ]
    db.session.add(pokemon)
    db.session.commit()
    return redirect(url_for("pokemon_index"))


@app.route("/pokemon/<int:poke_id>/edit/", methods=["GET", "POST"])
@login_required()
def edit_pokemon(poke_id):
    p = Pokemon.query.get(int(poke_id))
    form = PokeForm(request.form)
    errors = None
    if request.method == "POST" and form.validate():
        p.name = form.name.data
        p.poke_type = form.poke_type.data
        p.custom = form.custom.data
        p.description = form.description.data
        db.session.commit()
        return render_template("pokemon/specific.html", pokemon=p)
    return render_template("pokemon/edit.html", form=PokeForm(), pokemon=p)


@app.route("/pokemon/add_pokemon", methods=["GET", "POST"])
@login_required()
def add_pokemon():
    if (request.method == "GET"):
        return render_template(
            "pokemon/add_pokemon.html", form=DefaultPokemonForm())
    form = DefaultPokemonForm(request.form)
    pokemon = form.name.data
    user_id = current_user.get_id()
    user = User.query.filter_by(id=user_id).first()
    pokemon.accounts.append(user)
    db.session.add(pokemon)
    db.session.commit()
    return redirect(url_for("pokemon_index"))
