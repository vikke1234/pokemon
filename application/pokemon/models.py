from application import db

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    poke_type = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(300))
    custom = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, poke_type, description, custom):
        self.name = name
        self.poke_type = poke_type
        self.description = description
        self.custom = custom
