from flask import Flask
#!/usr/bin/python3
from flask_json import FlaskJSON, json_response
from flask_cors import CORS
import pusher

from .__pusher_config import PConfig
from .database import Database

app = Flask(__name__)
FlaskJSON(app)
CORS(app, resources=
    {
        r'/*': {'origins': '*'}
    }
)
db = Database()
event_pusher = pusher.Pusher(
    app_id=PConfig.app_id,
    key=PConfig.key,
    secret=PConfig.secret,
    cluster=PConfig.cluster,
    ssl=True
)
# TODO: ENGINE/SSL: create properly Signed SSL key and certificates
# TODO: ENGINE/SSL: implement SSL Context

from . import routes
