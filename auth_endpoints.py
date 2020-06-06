from flask import Flask, jsonify, request, Response, abort
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

app.config['JWT_SECRET_KEY'] = secret
jwt = JWTManager(app)

def does_user_exist(email: str) -> bool:
    users_collection.find_one({'email': email})
    return True

@app.route('/register', methods=['POST'])
def register():
    login_details = request.json
    errors = login_schema.validate(login_details)
    errors_str = return_errors_str(errors)
    if errors:
        abort(400, description=errors_str)
    users_collection.insert_one(login_details)
    return Response(None, 201)

@app.route('/login', methods=['POST'])
def login():
    login_details = request.json
    errors = login_schema.validate(login_details)
    errors_str = return_errors_str(errors)
    if errors:
        abort(400, description=errors_str)
    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=login_details, expires_delta=expires)
    login_details['access_token'] = access_token
    return Response(access_token, 200)

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200