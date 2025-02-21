from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_characters = db.Table(
    "favorite_characters",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("character_id", db.ForeignKey("character.id")),
)
favorite_planets = db.Table(
    "favorite_planets",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("planet_id", db.ForeignKey("planet.id")),
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False, unique=True)
    last_name = db.Column (db.String(250), nullable=False, unique=True)
    biography = db.Column (db.String(200), nullable=False, unique=False)
    password = db.Column(db.String(50), nullable=False, unique=False)
    favorite_planets = db.relationship("Planet", secondary="favorite_planets")
    favorite_characters = db.relationship("Character", secondary="favorite_characters")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "last_name": self.last_name,
            "name": self.name,
            "biography": self.biography,
            "favorite_planets": [planet.serialize()for planet in self.favorite_planets],
            "favorite_characters": [character.serialize()for character in self.favorite_characters]
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False) 

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
            # do not serialize the password, its a security breach
        }
