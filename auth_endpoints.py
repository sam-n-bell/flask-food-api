from flask import Flask, jsonify, request, Response, abort
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from __main__ import db, app
from marshmallow_models import LoginSchema, return_errors_str
import datetime
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

secret = os.getenv("jwt_secret")

login_schema = LoginSchema()

users_collection = db['users']
jwts_collection = db['jwts']

app.config['JWT_SECRET_KEY'] = secret
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


def get_existing_user(email: str):
    return users_collection.find_one({'email': email.lower()})

def does_user_exist(email: str) -> bool:
    user = users_collection.find_one({'email': email.lower()})
    if user is None:
        return False
    return True

@app.route('/register', methods=['POST'])
def register():
    login_details = request.json
    errors = login_schema.validate(login_details)
    errors_str = return_errors_str(errors)
    if errors:
        abort(400, description=errors_str)
    if does_user_exist(login_details['email']):
        abort(400, description="Account already exists")
    login_details['email'].lower()
    login_details['password'] = bcrypt.generate_password_hash(login_details['password'], 10)
    users_collection.insert_one(login_details)
    return Response(None, 201)

@app.route('/login', methods=['POST'])
def login():
    login_details = request.json
    errors = login_schema.validate(login_details)
    errors_str = return_errors_str(errors)
    if errors:
        abort(400, description=errors_str)
    user = get_existing_user(login_details['email'].lower())

    if not user:
        abort(400, description="Account not found")
    elif not bcrypt.check_password_hash(user['password'], login_details['password']):
        abort(401, description="Invalid email or password")

    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=login_details, expires_delta=expires)
    login_details['access_token'] = access_token

    jwt_dict = {
        'user': login_details['email'],
        'jwt': access_token,
        'created': datetime.datetime.utcnow()
    }
    jwts_collection.insert_one(jwt_dict)

    return Response(access_token, 200)

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200