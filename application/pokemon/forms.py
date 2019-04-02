from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SelectField, validators

class PokeForm(FlaskForm):
    __types = [
        ("normal", "Normal"),
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
        ("steel", "Steel")
    ]

    name = StringField("Pokemon name", [validators.Length(max=144)])
    description = TextAreaField("Description", [validators.Length(max=144)])
    poke_type = SelectField("type", choices=__types)
    custom = BooleanField("Custom")

    class Meta:
        csrf = False
