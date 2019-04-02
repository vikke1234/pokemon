from application import db
from application.models import Base
from application.pokemon.models import Pokemon
from application.pokemon.auth import User


def Arena(Base):
    __tablename__ = "arena"

    name = db.Column(db.String(30), nullable=False)
    custom_allowed = db.Column(db.Boolean, nullable=False)
    prize = db.Column(db.Integer)
    ranks = db.relationship("ranks", )

    def __init__(self, name, custom_allowed, prize):
        self.name = name
        self.custom_allowed = custom_allowed
        self.prize = self.prize


def Rank(Base):
    __tablename__ = "rank"

    account_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), nullable=False)
    leaderboard_id = db.Column(db.Integer, db.ForeignKey("arena.id"))

