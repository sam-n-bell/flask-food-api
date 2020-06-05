from flask import Flask
import pymongo
import ssl
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

uri = os.getenv("mongodb_uri")

client = pymongo.MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
db = client.foods_db

app = Flask(__name__)

import food_endpoints

if __name__ == '__main__':
    app.run(debug=True)