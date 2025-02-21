"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# user routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize()for user in users] 
    response_body = {
        "msg": "Here's a list of all the users",
        "users": serialized_users
    }

    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None : 
        return jsonify({"msg": "No user with that id was found"}), 404
    favorites = {
        "favorite_characters" : [character.serialize() for character in user.favorite_characters], 
        "favorite_planets" : [planet.serialize() for planet in user.favorite_planets]
    }

    response_body = {
        "msg": f"Here's the list of favorites for {user.name}",
        "favorites": favorites
    }

    return jsonify(response_body), 200


# characters routes
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize()for character in characters]
    response_body = {
        "msg": "Here's a list of all the characters",
        "characters": serialized_characters
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.filter_by(id=character_id).first()
    if character is None : 
        return jsonify({"msg": "No character with that id was found"}), 404
    response_body = {
        "msg": "Here's your character",
        "character": character.serialize()
    }

    return jsonify(response_body), 200

@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if user_id is None :
        return jsonify({"msg": "Please provide an available user_id"}), 400
    user = User.query.filter_by(id=user_id).first()
    if user is None : 
        return jsonify({"msg": "No user with that id was found"}), 404 
    character = Character.query.filter_by(id=character_id).first()
    if character is None : 
        return jsonify({"msg": "No character with that id was found"}), 404
    if character in user.favorite_characters : 
        return jsonify({"msg":"This character is already one of your favorites"}), 409
    user.favorite_characters.append(character)
    db.session.commit()
    db.session.refresh(user)
    return jsonify({"msg": "Congrats you succesfully added your favorite character"}), 200

@app.route('/favorite/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if user_id is None :
        return jsonify({"msg": "Please provide an available user_id"}), 400
    user = User.query.filter_by(id=user_id).first()
    if user is None : 
        return jsonify({"msg": "No user with that id was found"}), 404 
    character = Character.query.filter_by(id=character_id).first()
    if character is None : 
        return jsonify({"msg": "No character with that id was found"}), 404
    if character not in user.favorite_characters : 
        return jsonify({"msg":"This character is not one of your favorites"}), 409 
    user.favorite_characters.remove(character)
    db.session.commit()
    db.session.refresh(user)
    return jsonify({"msg": "Congrats you succesfully deleted your favorite character"}), 200

# planets routes
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize()for planet in planets] 
    response_body = {
        "msg": "Here's a list of all the planets",
        "planets": serialized_planets
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None : 
        return jsonify({"msg": "No planet with that id was found"}), 404
    response_body = {
        "msg": "Here's your planet",
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if user_id is None :
        return jsonify({"msg": "Please provide an user_id"}), 400
    user = User.query.filter_by(id=user_id).first()
    if user is None : 
        return jsonify({"msg": "No user with that id was found"}), 404 
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None : 
        return jsonify({"msg": "No planet with that id was found"}), 404
    if planet in user.favorite_planets : 
        return jsonify({"msg":"This planet is already one of your favorites"}), 409
    user.favorite_planets.append(planet)
    db.session.commit()
    db.session.refresh(user)
    return jsonify({"msg": "Congrats you succesfully added your favorite planet"}), 200

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if user_id is None :
        return jsonify({"msg": "Please provide an available user_id"}), 400
    user = User.query.filter_by(id=user_id).first()
    if user is None : 
        return jsonify({"msg": "No user with that id was found"}), 404 
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None : 
        return jsonify({"msg": "No planet with that id was found"}), 404
    if planet not in user.favorite_planets : 
        return jsonify({"msg":"This planet is not one of your favorites"}), 409 
    user.favorite_planets.remove(planet)
    db.session.commit()
    db.session.refresh(user)
    return jsonify({"msg": "Congrats you succesfully deleted your favorite planet"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
