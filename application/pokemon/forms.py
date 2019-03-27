from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField


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

    name = StringField("Pokemon name")
    description = TextAreaField("Description")
    poke_type = SelectField("type", choices=__types)
    custom = BooleanField("Custom")

    class Meta:
        csrf = False
