from application import db
from application.models import Base

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

user_moves = db.Table(
    "user_moves", Base.metadata,
    db.Column(
        "user_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
    db.Column(
        "move_id", db.Integer, db.ForeignKey("move.id"), primary_key=True))


class Pokemon(Base):
    __tablename__ = "pokemon"
    name = db.Column(db.String(20), nullable=False)
    poke_type = db.Column(db.String, nullable=False)
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

    @staticmethod
    def get_specific_pokemon(poke_id):
        if type(poke_id) is not int:
            raise TypeError("poke_id must be an integer")
        return Pokemon.query.get(poke_id)

    @staticmethod
    def get_user_pokemon(user_id):
        if type(user_id) is not int:
            raise TypeError("user_id must be an integer")
        return Pokemon.query.join(Pokemon.accounts).filter_by(id=user_id).all()

    @staticmethod
    def get_pokemon_moves(pokemon_id, user_id):
        if type(user_id) is not int or type(pokemon_id) is not int:
            raise TypeError("pokemon id and/or user id must be of type int")
        return Pokemon.query.join(Pokemon.move).all()


class Move(Base):
    """This is for having the possiblity to i.e. customize your pokemon further,
    but this is yet to be implented into the actual program."""

    __tablename__ = "move"
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(255))
    pokemon = db.relationship(
        "Pokemon", backref="move", secondary=pokemon_moves)
    account = db.relationship("User", backref="move", secondary=user_moves)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name

    @staticmethod
    def count_moves(pokemon_id, account_id):
        # Counts the amount of moves the specified pokemon
        # has on a given account
        statement = """
        SELECT COUNT(Move.id) FROM Move JOIN Pokemon_Moves ON Move.id = Pokemon_Moves.move_id
        JOIN Pokemon ON Pokemon.id = Pokemon_Moves.poke_id
        JOIN user_moves ON Move.id = user_moves.move_id
        JOIN Account ON Account.id = user_moves.user_id
        WHERE Pokemon.id = :poke_id AND Account.id = :account_id;
        """
        result = db.engine.execute(
            statement, poke_id=pokemon_id, account_id=account_id)
        return result.first()[0]
