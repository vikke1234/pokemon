from application import db
from application.models import Base
from application.auth.models import User


class Pokemon(Base):
    name = db.Column(db.String(20), nullable=False)
    poke_type = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300))
    custom = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), nullable=False)

    def __init__(self, name, poke_type, description, custom, account_id):
        self.name = name
        self.poke_type = poke_type
        self.description = description
        self.custom = custom
        self.account_id = account_id

    def get_user(self):
        return User.query.get(self.account_id)
