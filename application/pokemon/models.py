from application import db
from application.models import Base
from application.auth.models import User

association_table = db.Table(
    "poke_account", Base.metadata,
    db.Column(
        "pokemon_id",
        db.Integer,
        db.ForeignKey("pokemon.id"),
        primary_key=True),
    db.Column(
        "account_id",
        db.Integer,
        db.ForeignKey("account.id"),
        primary_key=True))

pokemon_moves = db.Table(
    "pokemon_moves", Base.metadata,
    db.Column(
        "poke_id", db.Integer, db.ForeignKey("pokemon.id"), primary_key=True),
    db.Column(
        "move_id", db.Integer, db.ForeignKey("move.id"), primary_key=True))


class Pokemon(Base):
    __tablename__ = "pokemon"
    name = db.Column(db.String(20), nullable=False)
    poke_type = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300))
    custom = db.Column(db.Boolean, nullable=False)
    accounts = db.relationship(
        "User", backref="pokemon", secondary=association_table)

    def __init__(self, name, poke_type, description, custom):
        self.name = name
        self.poke_type = poke_type
        self.description = description
        self.custom = custom

    def __repr__(self):
        return str(self.name) + ", id: " + str(self.id) + ", accounts: " + str(
            self.accounts)

    def __str__(self):
        return self.name


class Move(Base):
    __tablename__ = "move"
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(255))
    pokemon = db.relationship(
        "Pokemon", backref="move", secondary=pokemon_moves)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description
