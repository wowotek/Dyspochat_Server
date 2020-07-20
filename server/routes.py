from flask import jsonify
from . import app, json_response



@app.route('/ping', methods=['GET'])
def ping_pong():
    return json_response(data_='pong!')
