from flask import Flask
from flask_json import FlaskJSON, json_response
from flask_cors import CORS

from .database import Database


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

FlaskJSON(app)
CORS(app, resources={r'/*': {'origins': '*'}})


db = Database()

from . import routes