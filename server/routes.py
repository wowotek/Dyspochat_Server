from flask import jsonify, request
from flask_json import json_response
from . import app, db
from .models import User, Chat, Chatroom


@app.route('/ping', methods=['GET'])
def ping_pong():
    return json_response(data_='pong!')

@app.route('/user/register', methods=['POST'])
def user_register():
    ...

@app.route('/user/login', methods=['POST'])
def user_login():
    ...

@app.route('/user/unregister', methods=['POST'])
def user_unregister():
    user_id: int = int(request.form.get("user_id", type=int, default=-1))
    status = db.del_user_id(user_id)

    if status[0]:
        return json_response(
            data_={
                "status": "user_not_found",
                "user": None
            }
        )
        
    return json_response(
        data_={
            "status": "success",
            "user": {
                "id": status[1].id,
                "username": status[1].username,
                "pseudonym": status[1].pseudonym
            }
        }
    )

@app.route('/user/', methods=['GET'])
def user_get():
    user_id: int = int(request.form.get("user_id", type=int, default=-1))
    user: User = db.get_user_id(user_id)

    if user == None:
        return json_response(
            data_={
                "status": "user_not_found",
                "user": None
            }
        )

    return json_response(
        data_={
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username,
                "pseudonym": user.pseudonym
            }
        }
    )
