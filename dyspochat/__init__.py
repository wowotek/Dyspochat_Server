from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON

app = Flask("dyspochat-server")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tekoajaib123@localhost:3306/dyspochat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.environment = "development"
app.debug = True

db = SQLAlchemy(app)
json = FlaskJSON(app)

from . import route