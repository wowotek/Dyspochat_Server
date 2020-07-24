from functools import wraps

from flask import jsonify, request, abort
from flask_json import json_response

from . import app, db
from .models import User, Chat, Chatroom, Session, SessionData


################# API-KEY DECORATOR #################
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == "wowotek-key":
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
############### END API-KEY DECORATOR ###############

################# SESSION DECORATOR #################
def require_session(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-session-key') and request.headers.get('x-session-key') == "wowotek-key":
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
############### END SESSION DECORATOR ###############


@app.route('/ping', methods=['GET'])
def ping_pong():
    return json_response(data_='pong!')


################## USER BLUEPRINTS ##################
@app.route('/user', methods=['PUT'])
@require_appkey
def user_register():
    username: str = str(request.form.get("username", type=str))
    password: str = str(request.form.get("password", type=str))

    add_status = db.add_user(User(username, password))
    if add_status[0]:
        return json_response(
            data_={
                "status": "register_success",
                "user": {
                    "id": add_status[1].id,
                    "username": add_status[1].username
                }
            }
        )

    return json_response(
            data_={
                "status": "username_already_exist"
            }
        )


@app.route('/user', methods=['POST'])
@require_appkey
def user_login():
    username: str = str(request.form.get("username", type=str))
    password: str = str(request.form.get("password", type=str))

    user: User = db.get_user_username(username)
    if user != None:
        if user.password == password:
            session: Session = db.add_session()
            return json_response(
                data_={
                    "status": "login_success",
                    "session": {
                        "id": session.id,
                        "key": session.session_hash
                    }
                }
            )
        return json_response(
            data_={
                "status": "auth_failed"
            }
        )
    return json_response(
        data_={
            "status": "user_not_found"
        }
    )

@app.route('/user', methods=['DELETE'])
def user_unregister():
    user_id: int = int(request.form.get("user_id", type=int, default=-1))
    status = db.del_user_id(user_id)

    if status[0]:
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

    return json_response(
        data_={
            "status": "user_not_found"
        }
    )

@app.route('/user', methods=['GET'])
def user_get():
    user_id: int = int(request.form.get("user_id", type=int, default=-1))
    user: User = db.get_user_id(user_id)

    if user == None:
        return json_response(
            data_={
                "status": "user_not_found"
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
################ END USER BLUEPRINTS ################

################ CHATROOM BLUEPRINTS ################
@app.route('/chatroom', methods=['PUT'])
def chatroom_add():
    ...

@app.route('/chatroom', methods=['GET'])
def chatroom_get():
    ...

@app.route('/chatroom', methods=['DELETE'])
def chatroom_delete():
    ...

@app.route('/chatroom', methods=['POST'])
def chatroom_add_recipients():
    ...

@app.route('/chatroom', methods=['PATCH'])
def chatroom_del_recipients():
    ...
############## END CHATROOM BLUEPRINTS ##############

################## CHAT BLUEPRINTS ##################
@app.route('/chat', methods=['PUT'])
def chat_add():
    ...

@app.route('/chat', methods=['GET'])
def chat_get():
    ...
################ END CHAT BLUEPRINTS ################

################ SESSIONS BLUEPRINTS ################
@app.route('/sessions', methods=['PUT'])
def session_add_data():
    ...

@app.route('/session', methods=['GET'])
def session_get_data():
    ...

@app.route('/session', methods=['DELETE'])
def session_del_data():
    ...
############## END SESSIONS BLUEPRINTS ##############