from flask import Flask
from flask_json import FlaskJSON, json_response
from flask_cors import CORS

from .database import Database

app = Flask(__name__)

FlaskJSON(app)
CORS(app, resources={r'/*': {'origins': '*'}})

# TODO: ENGINE/SSL: create properly Signed SSL key and certificates
# TODO: ENGINE/SSL: implement SSL Context

db = Database()

from . import routes
