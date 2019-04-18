from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms import BooleanField, SelectField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from application.pokemon.models import Pokemon


def get_pokemon():
    return Pokemon.query.filter_by(custom=False)


class PokeForm(FlaskForm):
    __types = (("normal", "Normal"),
               ("fire", "Fire"),
               ("fighting", "Fighting"),
               ("water", "Water"),
               ("flying", "Flying"),
               ("grass", "Grass"),
               ("poison", "Poison"),
               ("electric", "Electric"),
               ("ground", "Ground"),
               ("psychic", "Psychic"),
               ("rock", "Rock"),
               ("ice", "Ice"),
               ("bug", "Bug"),
               ("dragon", "Dragon"),
               ("ghost", "Ghost"),
               ("dark", "Dark"),
               ("steel", "Steel"))  # yapf: disable
    name = StringField("Pokemon name", [validators.Length(min=2, max=144)])
    description = TextAreaField("Description", [validators.Length(max=144)])
    poke_type = SelectField("type", choices=__types)
    custom = BooleanField("Custom")

    class Meta:
        csrf = False


class Search(FlaskForm):
    search = StringField()
    submit = SubmitField()

    class Meta:
        csrf = False


# TODO add like filters and shit
class DefaultPokemonForm(FlaskForm):
    name = QuerySelectField(
        "Pokemon",
        validators=[validators.Required()],
        query_factory=get_pokemon)

    class Meta:
        csrf = False
