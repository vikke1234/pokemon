from application import db

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    poke_type = db.Column(db.String(10), nullable=False)

    def __init__(self, name, poke_type):
        self.name = name
        self.poke_type = poke_type
