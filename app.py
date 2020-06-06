from flask import Flask, jsonify
import pymongo
import ssl
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

uri = os.getenv("mongodb_uri")

client = pymongo.MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
db = client.foods_db

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_system_error(e):
    return jsonify(error=str(e)), 500

import food_endpoints
import auth_endpoints

if __name__ == '__main__':
    app.run(debug=True)
