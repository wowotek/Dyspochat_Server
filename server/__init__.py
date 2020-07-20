from flask import Flask
from flask_json import FlaskJSON, json_response
from flask_cors import CORS


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

FlaskJSON(app)
CORS(app, resources={r'/*': {'origins': '*'}})


from . import routes